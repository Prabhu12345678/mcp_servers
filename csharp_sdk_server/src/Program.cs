using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using ModelContextProtocol.Server;
using ModelContextProtocol.Server.Tool;
using ModelContextProtocol.Types;

namespace McpAddServer
{
    internal class Program
    {
        private static async Task Main(string[] args)
        {
            // ---- Tool definition ------------------------------------------------
            var addTool = new Tool(
                name: "add",
                description: "Return the sum of two numbers.",
                inputSchema: JsonSchema.Object(
                    properties: new Dictionary<string, JsonSchema>
                    {
                        ["a"] = JsonSchema.Number(),
                        ["b"] = JsonSchema.Number()
                    },
                    required: new[] { "a", "b" }
                )
            );

            // ---- Server construction (stdio transport is default) -------------
            var server = McpServerBuilder.Create()
                .WithServerName("example-add-server")
                .WithServerVersion("0.1.0")
                .WithTool(addTool, HandleAddTool)
                .Build();

            // ---- Run server ----------------------------------------------------
            await server.RunAsync(
                new InitializationOptions(),
                new NotificationOptions()
            );
        }

        private static Task<IReadOnlyList<Content>> HandleAddTool(
            string toolName,
            IReadOnlyDictionary<string, JsonValue> arguments)
        {
            if (toolName != "add")
                throw new ArgumentException($"Unknown tool: {toolName}");

            double a = ((JsonValue.Number)arguments["a"]).GetValue<double>();
            double b = ((JsonValue.Number)arguments["b"]).GetValue<double>();
            double result = a + b;

            var text = new TextContent(
                $"The sum of {a} and {b} is {result}."
            );

            return Task.FromResult<IReadOnlyList<Content>>(new List<Content> { text });
        }
    }
}