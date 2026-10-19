## Architecture

1. **Server object** (`mcp.server.Server`) handles the MCP lifecycle.
2. **Tool registration** via `@server.list_tools` and `@server.call_tool`.
3. **Transport** – the `server.run(...)` call wires JSON‑RPC over standard input/output.
4. **Tool implementation** – simple addition returning a `TextContent`.