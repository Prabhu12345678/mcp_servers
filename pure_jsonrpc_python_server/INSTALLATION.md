## Installation & Usage

1. **Prerequisites**: Python 3.8+.
2. **Clone** the folder (or copy the files).
3. **Make the script executable** (optional):
   ```bash
   chmod +x src/pure_mcp_server.py
   ```
4. **Run**:
   ```bash
   python src/pure_mcp_server.py
   ```
5. **Test** (install MCP CLI once):
   ```bash
   cargo install mcp-cli
   mcp client --server python src/pure_mcp_server.py
   ```
   Inside the client prompt:
   ```
   > tools/add {"a": 10, "b": 20}
   The sum of 10.0 and 20.0 is 30.0.
   ```
6. Stop with `Ctrl+C`.