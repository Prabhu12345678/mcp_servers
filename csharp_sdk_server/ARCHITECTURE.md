## Architecture

1. **McpServerBuilder** creates the server and registers the tool.
2. **Tool** object defines the name, description, and JSON‑Schema.
3. **Handler delegate** (`HandleAddTool`) performs the addition and returns a `TextContent`.
4. **Server.RunAsync** starts the JSON‑RPC stdio loop.