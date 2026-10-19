#!/usr/bin/env python3
"""
MCP client that talks to a locally‑running LLM exposed as an MCP tool.

Assumptions about the server:
  - It provides a tool named "generate".
  - The tool expects a single argument: { "prompt": "<text>" }.
  - It returns a list of Content objects; we only need the first TextContent.
  - Transport: stdio (the server is launched as a subprocess).
"""

import asyncio
import sys
from mcp.client.stdio import stdio_client   # stdio transport helper
from mcp import ClientSession               # high‑level MCP session

def show_reply(result):
    """Extract the textual reply from the MCP CallToolResult."""
    for part in result.content:
        if part.type == "text":
            print("\n🤖 Assistant:", part.text)
            return
    print("\n🤖 Assistant (raw):", result.content)

async def main():
    # --------------------------------------------------------------
    # 1️⃣ Launch the MCP server as a subprocess.
    #    Replace the command/args with whatever starts your LLM‑server.
    #    Example: a server that wraps Ollama's /api/generate endpoint.
    # --------------------------------------------------------------
    server_params = {
        "command": "python",          # or "node", "dotnet", etc.
        "args": ["mcp_llm_server.py"] # <-- your server script
    }

    # --------------------------------------------------------------
    # 2️⃣ Create a stdio‑based MCP client session.
    # --------------------------------------------------------------
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialise the MCP session (exchange serverInfo, capabilities, etc.)
            await session.initialize()

            # ------------------------------------------------------
            # 3️⃣ Simple REPL: read a prompt from the user, call the tool,
            #    print the model's answer, repeat until Ctrl‑C or "exit".
            # ------------------------------------------------------
            print("💬 MCP‑LLM client ready. Type your prompt (or 'exit' to quit).")
            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n👋 Bye!")
                    break

                if not user_input:
                    continue
                if user_input.lower() in {"exit", "quit"}:
                    print("👋 Bye!")
                    break

                # Call the "generate" tool on the server.
                try:
                    call_result = await session.call_tool(
                        name="generate",
                        arguments={"prompt": user_input}
                    )
                    show_reply(call_result)
                except Exception as e:
                    print(f"❌ Error calling tool: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted – exiting.")