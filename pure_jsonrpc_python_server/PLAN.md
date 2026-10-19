## Implementation Plan

1. Write a `send_message` helper that writes JSON‑RPC objects to stdout.
2. Define static server info and tool list (as JSON‑compatible dicts).
3. Implement `tool_add`.
4. In the main loop:
   * Read a line, parse JSON.
   * Validate JSON‑RPC version.
   * Dispatch to the appropriate handler.
   * Send back a JSON‑RPC response.
5. Test with an MCP client (e.g., the `mcp` CLI or the Python client shown elsewhere).