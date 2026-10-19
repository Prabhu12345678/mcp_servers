use modelcontextprotocol::{
    server::{McpServer, McpServerBuilder},
    types::{
        Content, JsonValue, TextContent,
        tool::Tool,
        InitializationOptions, NotificationOptions,
    },
};
use std::convert::Infallible;
use std::sync::Arc;

#[tokio::main]
async fn main() -> Result<(), Infallible> {
    // ---- Tool definition ----------------------------------------------------
    let add_tool = Tool::new(
        "add".to_string(),
        "Return the sum of two numbers.".to_string(),
        serde_json::json!({
            "type": "object",
            "properties": {
                "a": { "type": "number", "description": "First addend" },
                "b": { "type": "number", "description": "Second addend" }
            },
            "required": ["a", "b"]
        }),
        Arc::new(move |_name: &str, args: &serde_json::Map<String, JsonValue>| {
            let a = args.get("a").and_then(JsonValue::as_f64).unwrap_or(0.0);
            let b = args.get("b").and_then(JsonValue::as_f64).unwrap_or(0.0);
            let result = a + b;
            let text = TextContent::new(format!(
                "The sum of {} and {} is {}.",
                a, b, result
            ));
            std::future::ready(Ok(vec![Content::Text(text)]))
        }),
    );

    // ---- Server construction (stdio transport is default) -------------------
    let server = McpServerBuilder::new()
        .server_name("example-add-server")
        .server_version("0.1.0")
        .add_tool(add_tool)
        .build();

    // ---- Run server ---------------------------------------------------------
    server
        .run(InitializationOptions::default(), NotificationOptions::default())
        .await
        .expect("MCP server failed");

    Ok(())
}