package org.example;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

/**
 * Pure JSON‑RPC 2.0 MCP server (stdio transport).
 *
 * Implements only:
 *   - initialize
 *   - tools/list
 *   - tools/call (only the "add" tool)
 */
public class PureMcpServer {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    // Server info (same as in the SDK examples)
    private static final ObjectNode SERVER_INFO;
    static {
        SERVER_INFO = MAPPER.createObjectNode();
        SERVER_INFO.put("protocolVersion", "2024-11-05");
        ObjectNode serverInfo = SERVER_INFO.putObject("serverInfo");
        serverInfo.put("name", "pure-mcp-server-java");
        serverInfo.put("version", "0.1.0");
        ObjectNode caps = SERVER_INFO.putObject("capabilities");
        caps.putObject("tools");
    }

    // Tool list (only the add tool)
    private static final ArrayNode TOOLS;
    static {
        TOOLS = MAPPER.createArrayNode();
        ObjectNode add = TOOLS.addObject();
        add.put("name", "add");
        add.put("description", "Return the sum of two numbers.");
        ObjectNode schema = add.putObject("inputSchema");
        schema.put("type", "object");
        ObjectNode props = schema.putObject("properties");
        props.putObject("a")
             .put("type", "number")
             .put("description", "First addend");
        props.putObject("b")
             .put("type", "number")
             .put("description", "Second addend");
        ArrayNode required = schema.putArray("required");
        required.add("a").add("b");
    }

    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter writer = new PrintWriter(System.out, true); // auto‑flush

        String line;
        while ((line = reader.readLine()) != null) {
            if (line.isEmpty()) continue;

            JsonNode request;
            try {
                request = MAPPER.readTree(line);
            } catch (IOException e) {
                sendError(writer, null, -32700, "Parse error", e.getMessage());
                continue;
            }

            // Basic JSON‑RPC validation
            if (!request.has("jsonrpc") ||
                !request.get("jsonrpc").asText().equals("2.0")) {
                sendError(writer,
                        request.has("id") ? request.get("id") : MAPPER.nullNode(),
                        -32600, "Invalid Request",
                        "Missing or incorrect jsonrpc version");
                continue;
            }

            JsonNode idNode = request.has("id") ? request.get("id") : MAPPER.nullNode();
            String method = request.has("method") ? request.get("method").asText() : "";
            JsonNode params = request.has("params") ? request.get("params") : MAPPER.createObjectNode();

            ObjectNode response = MAPPER.createObjectNode();
            response.put("jsonrpc", "2.0");
            response.set("id", idNode.deepCopy());

            try {
                ObjectNode result;
                switch (method) {
                    case "initialize":
                        result = (ObjectNode) SERVER_INFO.deepCopy();
                        break;
                    case "tools/list":
                        result = MAPPER.createObjectNode()
                                .set("tools", TOOLS.deepCopy());
                        break;
                    case "tools/call":
                        String toolName = params.has("name")
                                ? params.get("name").asText() : "";
                        JsonNode argsNode = params.has("arguments")
                                ? params.get("arguments") : MAPPER.createObjectNode();

                        if (!"add".equals(toolName)) {
                            throw new IllegalArgumentException("Unknown tool: " + toolName);
                        }

                        // Very lightweight validation (just check existence & numeric)
                        double a = argsNode.has("a") ? argsNode.get("a").asDouble(0.0) : 0.0;
                        double b = argsNode.has("b") ? argsNode.get("b").asDouble(0.0) : 0.0;
                        double sum = a + b;

                        ObjectNode content = MAPPER.createObjectNode()
                                .put("type", "text")
                                .put("text", "The sum of " + a + " and " + b + " is " + sum + ".");

                        ArrayNode contentArray = MAPPER.createArrayNode();
                        contentArray.add(content);

                        result = MAPPER.createObjectNode()
                                .set("content", contentArray);
                        break;
                    default:
                        throw new IllegalArgumentException("Method not found: " + method);
                }
                response.set("result", result);
            } catch (IllegalArgumentException e) {
                int code = e.getMessage().startsWith("Unknown tool")
                        ? -32602   // Invalid params
                        : -32601;  // Method not found
                sendError(writer, idNode, code, e.getMessage(), null);
                continue;
            } catch (Exception e) {
                sendError(writer, idNode, -32603, "Internal error", e.getMessage());
                continue;
            }

            writer.println(MAPPER.writeValueAsString(response));
        }
    }

    private static void sendError(PrintWriter writer,
                                  JsonNode id,
                                  int code,
                                  String message,
                                  String data) {
        ObjectNode error = MAPPER.createObjectNode()
                .put("code", code)
                .put("message", message);
        if (data != null) {
            error.put("data", data);
        }
        ObjectNode resp = MAPPER.createObjectNode();
        resp.put("jsonrpc", "2.0");
        resp.set("id", id == null ? MAPPER.nullNode() : id);
        resp.set("error", error);
        writer.println(MAPPER.writeValueAsString(resp));
    }
}