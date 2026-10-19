#!/usr/bin/env python3
"""
A tiny MCP server written with the official Python SDK.

Features:
- JSON‑RPC over stdio (the default transport for local MCP servers)
- One tool: `add(a, b) -> number`
"""

import asyncio
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)


async def handle_list_tools():
    return [
        Tool(
            name="add",
            description="Return the sum of two numbers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First addend"},
                    "b": {"type": "number", "description": "Second addend"},
                },
                "required": ["a", "b"],
            },
        )
    ]


async def handle_call_tool(name: str, arguments: dict):
    if name == "add":
        a = float(arguments.get("a", 0))
        b = float(arguments.get("b", 0))
        result = a + b
        return [
            TextContent(
                type="text",
                text=f"The sum of {a} and {b} is {result}.",
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_set_logging_level(level: LoggingLevel):
    pass


async def main():
    # Create server instance with handler functions
    server = Server(
        "example-add-server",
        on_list_tools=handle_list_tools,
        on_call_tool=handle_call_tool,
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example-add-server",
                server_version="0.1.0",
                capabilities={},  # Add empty capabilities dict
            ),
            NotificationOptions(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
