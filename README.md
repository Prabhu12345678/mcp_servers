# MCP Samples Repository

This repository contains educational examples of MCP (Model Context Protocol) servers and clients in various languages, both using the official SDKs and pure JSON‑RPC implementations.

## Directory Structure

Each language/variant has its own folder:

- `python_sdk_server/` – Python server using the official MCP Python SDK
- `java_sdk_server/` – Java server using the official MCP Java SDK
- `csharp_sdk_server/` – C# server using the official MCP .NET SDK
- `rust_sdk_server/` – Rust server using the official MCP Rust SDK
- `pure_jsonrpc_python_server/` – Python server implementing MCP via raw JSON‑RPC (no SDK)
- `pure_java_server/` – Java server implementing MCP via raw JSON‑RPC (no SDK, uses Jackson)
- `pure_csharp_server/` – C# server implementing MCP via raw JSON‑RPC (no SDK, uses System.Text.Json)
- `python_client/` – Python client that connects to an MCP server exposing a `generate` tool (for local LLM integration)

Each folder contains:
- Source code in `src/`
- `README.md` – brief description
- `ARCHITECTURE.md` – high‑level design
- `PLAN.md` – implementation steps
- `INSTALLATION.md` – build/run/test instructions

## Testing the Servers

A generic test script `test_mcp_server.py` is provided at the repository root. It launches a server as a subprocess and verifies the three core MCP methods (`initialize`, `tools/list`, `tools/call` for the `add` tool).

To test a specific server, run:

```bash
python test_mcp_server.py --command "<launch command>"
```

### Example commands for each server

**Python SDK Server**
```bash
python test_mcp_server.py --command "python python_sdk_server/src/mcp_add_server.py"
```

**Java SDK Server**
```bash
python test_mcp_server.py --command "java -jar java_sdk_server/target/mcp-add-server-java-1.0-SNAPSHOT.jar"
```
*(You must first build the jar with `mvn clean package` in the `java_sdk_server` folder.)*

**C# SDK Server**
```bash
python test_mcp_server.py --command "dotnet run --project csharp_sdk_server/McpAddServer.csproj"
```

**Rust SDK Server**
```bash
python test_mcp_server.py --command "cargo run --release --manifest-path rust_sdk_server/Cargo.toml"
```

**Pure JSON‑RPC Python Server**
```bash
python test_mcp_server.py --command "python pure_jsonrpc_python_server/src/pure_mcp_server.py"
```

**Pure Java Server**
```bash
python test_mcp_server.py --command "java -jar pure_java_server/target/pure-mcp-server-java-1.0-SNAPSHOT.jar"
```
*(Build with `mvn clean package` in `pure_java_server` first.)*

**Pure C# Server**
```bash
python test_mcp_server.py --command "dotnet run --project pure_csharp_server/PureMcpServerCs.csproj"
```

## Notes

- The test script expects the server to communicate over stdio (JSON‑RPC 2.0), which is the default for all the provided examples.
- For the `python_client` folder, see its own `README.md` for how to run the client against a local LLM‑wrapper server.

Enjoy exploring MCP across languages!