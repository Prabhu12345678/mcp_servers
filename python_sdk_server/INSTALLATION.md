## Installation & Usage

1. **Clone** this repository (or copy the folder).
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install mcp
   ```
4. **Run the server**:
   ```bash
   python src/mcp_add_server.py
   ```
5. **Test** with the MCP CLI (install once):
   ```bash
   cargo install mcp-cli   # provides the `mcp` command
   mcp client --server python src/mcp_add_server.py
   ```
   Then inside the client prompt:
   ```
   > tools/add {"a": 5, "b": 7}
   The sum of 5.0 and 7.0 is 12.0.
   ```
6. To stop the server, press `Ctrl+C`.