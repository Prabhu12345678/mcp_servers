## Architecture

1. **McpServerBuilder** creates the server, sets name/version.
2. **ToolProvider** lambda implements the tool logic.
3. **McpServer.run** starts the JSON‑RPC message loop over stdio.
4. The server returns a `List<TextContent>` from the tool call.