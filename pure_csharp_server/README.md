# Pure JSON‑RPC C# MCP Server

A hand‑rolled MCP server that implements only the required RPC methods (`initialize`, `tools/list`, `tools/call`) for an `add` tool. No MCP SDK is used—only `System.Text.Json`.

*Transport*: stdio (JSON‑RPC 2.0)  
*Language*: C# 10 (.NET 8)  
*Dependencies*: None beyond the .NET SDK