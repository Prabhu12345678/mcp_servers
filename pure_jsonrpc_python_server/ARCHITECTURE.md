## Architecture

1. **Message loop** reads one JSON line per request from stdin.
2. **Dispatch** on the `"method"` field to three handlers.
3. **Handlers** return the appropriate JSON‑RPC response (`result` or `error`).
4. **Tool implementation** – `tool_add` performs the addition and returns an MCP `Content` list.