## Implementation Plan

1. Install the `mcp` SDK (`pip install mcp`).
2. Create a `Server` instance.
3. Decorate `list_tools` to return the `add` tool definition.
4. Decorate `call_tool` to implement the addition logic.
5. Start the server with `server.run()` over stdio.
6. Test with an MCP client (e.g., the `mcp` CLI or the Python client provided elsewhere).