package org.example;

import modelcontextprotocol.sdk.server.McpServer;
import modelcontextprotocol.sdk.server.McpServerBuilder;
import modelcontextprotocol.sdk.server.notification.NotificationOptions;
import modelcontextprotocol.sdk.server.initialization.InitializationOptions;
import modelcontextprotocol.sdk.server.tool.Tool;
import modelcontextprotocol.sdk.server.tool.ToolProvider;
import modelcontextprotocol.sdk.types.TextContent;
import modelcontextprotocol.sdk.types.CallToolResult;
import modelcontextprotocol.sdk.types.JsonValue;

import java.util.List;
import java.util.Map;

public class McpAddServer {

    public static void main(String[] args) throws Exception {
        // ---- Tool definition -------------------------------------------------
        ToolProvider addTool = (name, arguments) -> {
            if (!"add".equals(name)) {
                throw new IllegalArgumentException("Unknown tool: " + name);
            }

            double a = ((JsonValue.Number) arguments.get("a")).doubleValue();
            double b = ((JsonValue.Number) arguments.get("b")).doubleValue();
            double result = a + b;

            return List.of(
                new TextContent(
                    "The sum of " + a + " and " + b + " is " + result + "."
                )
            );
        };

        // ---- Server construction (stdio transport is default) ---------------
        McpServer server = McpServerBuilder.builder()
                .serverName("example-add-server")
                .serverVersion("0.1.0")
                .addTool("add", "Return the sum of two numbers.", addTool)
                .build();

        // ---- Run server ------------------------------------------------------
        server.run(
                new InitializationOptions(),
                new NotificationOptions()
        ).join(); // blocks until interrupted
    }
}