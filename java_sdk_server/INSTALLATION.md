## Installation & Usage

1. **Prerequisites**: JDK 17+, Maven.
2. **Clone** the folder (or copy the files).
3. **Build**:
   ```bash
   mvn clean package
   ```
   The executable jar will be at `target/mcp-add-server-java-1.0-SNAPSHOT.jar`.
4. **Run**:
   ```bash
   java -jar target/mcp-add-server-java-1.0-SNAPSHOT.jar
   ```
5. **Test** (install the MCP CLI once):
   ```bash
   cargo install mcp-cli
   mcp client --server java -jar target/mcp-add-server-java-1.0-SNAPSHOT.jar
   ```
   Inside the client prompt:
   ```
   > tools/add {"a": 3, "b": 4}
   The sum of 3.0 and 4.0 is 7.0.
   ```
6. Stop with `Ctrl+C`.