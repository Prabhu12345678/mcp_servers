# Pure JSON‑RPC Java MCP Server

A hand‑rolled MCP server that implements only the required RPC methods (`initialize`, `tools/list`, `tools/call`) for an `add` tool. No MCP SDK is used—only Jackson for JSON.

*Transport*: stdio (JSON‑RPC 2.0)  
*Language*: Java 17+  
*Dependency*: `jackson-databind` (Maven)