## Installation & Usage

1. **Prerequisites**: Rust toolchain (via `rustup`).
2. **Clone** the folder (or copy the files).
3. **Build**:
   ```bash
   cargo build --release
   ```
4. **Run**:
   ```bash
   cargo run --release
   ```
5. **Test** (install MCP CLI once):
   ```bash
   cargo install mcp-cli
   mcp client --server cargo run --release
   ```
   Inside the client prompt:
   ```
   > tools/add {"a": 1.2, "b": 3.4}
   The sum of 1.2 and 3.4 is 4.6.
   ```
6. Stop with `Ctrl+C`.