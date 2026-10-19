## Architecture

1. **Message loop** reads a line from stdin, parses with Jackson.
2. **Dispatch** on the `"method"` field.
3. **Handlers** return JSON‑RPC responses (result or error) as Jackson `ObjectNode`.
4. **Tool implementation** builds an MCP `Content` list with a single `TextContent`.