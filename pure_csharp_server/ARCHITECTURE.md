## Architecture

1. **Message loop** reads a line from stdin, deserializes to `JsonRpcRequest`.
2. **Dispatch** on the `Method` field.
3. **Handlers** build a `JsonRpcResponse` (result or error) and serialize it to stdout.
4. **Tool implementation** extracts `a` and `b`, adds them, returns an MCP `TextContent` wrapped in a JSON array under the `content` key.