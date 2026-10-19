## Architecture

1. **McpServerBuilder** creates the server, sets name/version.
2. **Tool::new** builds the tool with its JSON‑Schema and an async handler.
3. The handler extracts `a` and `b` as `f64`, adds them, and returns a `TextContent`.
4. `McpServer::run` starts the JSON‑RPC stdio loop.