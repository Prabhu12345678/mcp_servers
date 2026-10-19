## Implementation Plan

1. Add `modelcontextprotocol-rust` and `tokio` to `Cargo.toml`.
2. Define the `add` tool using `Tool::new`.
3. Implement the async handler that parses arguments, adds numbers, and returns `TextContent`.
4. Build the server with `McpServerBuilder`.
5. Call `server.run()` to start the stdio JSON‑RPC loop.
6. Build with `cargo build --release` and run with `cargo run --release`.
7. Test using the `mcp` CLI.