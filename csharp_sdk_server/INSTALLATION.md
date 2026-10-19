## Installation & Usage

1. **Prerequisites**: .NET 8 SDK.
2. **Clone** the folder (or copy the files).
3. **Restore dependencies**:
   ```bash
   dotnet restore
   ```
4. **Build & run**:
   ```bash
   dotnet run --project McpAddServer.csproj
   ```
5. **Test** (install MCP CLI once):
   ```bash
   cargo install mcp-cli
   mcp client --server dotnet run --project McpAddServer.csproj
   ```
   Inside the client prompt:
   ```
   > tools/add {"a": 2.5, "b": 3.5}
   The sum of 2.5 and 3.5 is 6.0.
   ```
6. Stop with `Ctrl+C`.