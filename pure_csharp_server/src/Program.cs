using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace PureMcpServerCs
{
    // -----------------------------------------------------------------
    // DTOs for JSON‑RPC MCP messages (only what we need)
    // -----------------------------------------------------------------
    public class JsonRpcRequest
    {
        [JsonPropertyName("jsonrpc")] public string JsonRpc { get; set; } = "2.0";
        [JsonPropertyName("id")] public JsonElement? Id { get; set; }
        [JsonPropertyName("method")] public string Method { get; set; } = "";
        [JsonPropertyName("params")] public JsonElement? Params { get; set; }
    }

    public class JsonRpcResponse
    {
        [JsonPropertyName("jsonrpc")] public string JsonRpc { get; set; } = "2.0";
        [JsonPropertyName("id")] public JsonElement? Id { get; set; }
        [JsonPropertyName("result")] public JsonElement? Result { get; set; }
        [JsonPropertyName("error")] public JsonRpcError? Error { get; set; }
    }

    public class JsonRpcError
    {
        [JsonPropertyName("code")] public int Code { get; set; }
        [JsonPropertyName("message")] public string Message { get; set; } = "";
        [JsonPropertyName("data")] public string? Data { get; set; }
    }

    // -----------------------------------------------------------------
    // Static server info and tool list (same as SDK examples)
    // -----------------------------------------------------------------
    private static readonly JsonElement ServerInfo;
    private static readonly JsonElement ToolsList;

    static PureMcpServerCs()
    {
        using var doc = JsonDocument.Parse(@"""
        {
            ""protocolVersion"": ""2024-11-05"",
            ""serverInfo"": {
                ""name"": ""pure-mcp-server-cs"",
                ""version"": ""0.1.0""
            },
            ""capabilities"": {
                ""tools"": {}
            }
        }
        """);
        ServerInfo = doc.RootElement.Clone();

        using var toolsDoc = JsonDocument.Parse(@"""
        [
            {
                ""name"": ""add"",
                ""description"": ""Return the sum of two numbers."",
                ""inputSchema"": {
                    ""type"": ""object"",
                    ""properties"": {
                        ""a"": { ""type"": ""number"", ""description"": ""First addend"" },
                        ""b"": { ""type"": ""number"", ""description"": ""Second addend"" }
                    },
                    ""required"": [""a"",""b""]
                }
            }
        ]
        """);
        ToolsList = toolsDoc.RootElement.Clone();
    }

    // -----------------------------------------------------------------
    // Main stdio loop
    // -----------------------------------------------------------------
    public static void Main()
    {
        var options = new JsonSerializerOptions { WriteIndented = false };
        using var input  = new StreamReader(Console.OpenStandardInput());
        using var output = new StreamWriter(Console.OpenStandardOutput()) { AutoFlush = true };

        string? line;
        while ((line = input.ReadLine()) != null)
        {
            if (string.IsNullOrWhiteSpace(line)) continue;

            JsonRpcRequest? request;
            try
            {
                request = JsonSerializer.Deserialize<JsonRpcRequest>(line, options);
            }
            catch (JsonException)
            {
                SendError(output, null, -32700, "Parse error", "Invalid JSON");
                continue;
            }

            if (request == null || request.JsonRpc != "2.0")
            {
                SendError(output, request?.Id, -32600, "Invalid Request",
                          "Missing or incorrect jsonrpc version");
                continue;
            }

            var id = request.Id ?? JsonElement.Null;
            var method = request.Method;
            var pars = request.Params ?? JsonElement.Null;

            var response = new JsonRpcResponse { JsonRpc = "2.0", Id = id };

            try
            {
                JsonElement result;
                switch (method)
                {
                    case "initialize":
                        result = ServerInfo;
                        break;
                    case "tools/list":
                        var obj = new JsonObject();
                        obj.Add("tools", ToolsList);
                        result = JsonValue.CreateObject(obj);
                        break;
                    case "tools/call":
                        string toolName = pars.TryGetProperty("name", out JsonElement name) && name.ValueKind == JsonValueKind.String
                                            ? name.GetString()! : "";
                        JsonElement args = pars.TryGetProperty("arguments", out JsonElement a) && a.ValueKind == JsonValueKind.Object
                                            ? a : new JsonObject();

                        if (!"add".Equals(toolName, StringComparison.OrdinalIgnoreCase))
                            throw new ArgumentException($"Unknown tool: {toolName}");

                        double aVal = 0.0, bVal = 0.0;
                        if (args.TryGetProperty("a", out JsonElement aProp) && aProp.ValueKind == JsonValueKind.Number)
                            aVal = aProp.GetDouble();
                        if (args.TryGetProperty("b", out JsonElement bProp) && bProp.ValueKind == JsonValueKind.Number)
                            bVal = bProp.GetDouble();

                        double sum = aVal + bVal;
                        var contentObj = new JsonObject
                        {
                            ["type"] = JsonValue.CreateStringValue("text"),
                            ["text"] = JsonValue.CreateStringValue(
                                            $"The sum of {aVal} and {bVal} is {sum}.")
                        };
                        var contentArray = new JsonArray { JsonValue.CreateObjectValue(contentObj) };

                        var resultObj = new JsonObject { ["content"] = JsonValue.CreateArrayValue(contentArray) };
                        result = JsonValue.CreateObjectValue(resultObj);
                        break;
                    default:
                        throw new ArgumentException($"Method not found: {method}");
                }
                response.Result = result;
            }
            catch (ArgumentException ex) when (ex.Message.StartsWith("Unknown tool"))
            {
                SendError(output, id, -32602, "Invalid params", ex.Message);
                continue;
            }
            catch (ArgumentException ex)
            {
                SendError(output, id, -32601, "Method not found", ex.Message);
                continue;
            }
            catch (Exception ex)
            {
                SendError(output, id, -32603, "Internal error", ex.Message);
                continue;
            }

            string outJson = JsonSerializer.Serialize(response, options);
            output.WriteLine(outJson);
        }
    }

    private static void SendError(TextWriter writer,
                                  JsonElement id,
                                  int code,
                                  string message,
                                  string? data)
    {
        var error = new JsonObject
        {
            ["code"] = JsonValue.CreateNumberValue(code),
            ["message"] = JsonValue.CreateStringValue(message)
        };
        if (data != null)
            error["data"] = JsonValue.CreateStringValue(data);

        var resp = new JsonObject
        {
            ["jsonrpc"] = JsonValue.CreateStringValue("2.0"),
            ["id"] = id.ValueKind == JsonValueKind.Null ? JsonValue.Null : id,
            ["error"] = JsonValue.CreateObjectValue(error)
        };
        writer.WriteLine(JsonSerializer.Serialize(resp, new JsonSerializerOptions { WriteIndented = false }));
    }
}