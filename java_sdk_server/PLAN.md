## Implementation Plan

1. Add the MCP Java SDK as a Maven dependency.
2. Create a `McpServerBuilder` instance.
3. Register the `add` tool via `addTool`.
4. Implement the tool logic inside a `ToolProvider` lambda.
5. Call `server.run()` to start the stdio JSON‑RPC loop.
6. Build with `mvn package` and run with `java -jar`.
7. Test using the `mcp` CLI or any MCP client.