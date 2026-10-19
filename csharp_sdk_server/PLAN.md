## Implementation Plan

1. Create a new console project (`dotnet new console`).
2. Add the NuGet package `ModelContextProtocol.Sdk`.
3. Define the `add` tool with its JSON‑Schema.
4. Provide a delegate that implements the addition logic.
5. Build the server with `McpServerBuilder.Create()`.
6. Call `RunAsync` to start listening on stdio.
7. Build/run with `dotnet run`.
8. Test using the `mcp` CLI or any MCP client.