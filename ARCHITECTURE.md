# Model Context Protocol (MCP) Server Architecture

## Overview

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). MCP servers expose capabilities (tools, resources, prompts) that LLMs can discover and use through a standardized interface.

## Core Concepts

### Transport Layer
MCP defines how clients and servers communicate. The most common transport for local development is:
- **stdio**: JSON-RPC 2.0 messages over standard input/output streams
- Other transports (HTTP, WebSocket) are possible but less common in the examples

### JSON-RPC 2.0 Foundation
All MCP communication uses JSON-RPC 2.0:
- Requests contain `jsonrpc: "2.0"`, `method`, `params`, and `id`
- Responses contain `jsonrpc: "2.0"`, `result` (or `error`), and matching `id`
- Notifications omit the `id` field
- Error codes follow JSON-RPC 2.0 standards

### Server Capabilities
During initialization, servers advertise their capabilities:
- `tools`: Server can expose callable functions
- `resources`: Server can expose readable data sources
- `prompts`: Server can expose prompt templates
- `logging`: Server can send log messages to client

### Tools
Tools are functions that LLMs can invoke:
- Defined with a name, description, and JSON Schema input specification
- Invoked via `tools/call` method with tool name and arguments
- Return structured content (text, images, embedded resources)
- Must handle unknown tools and invalid arguments gracefully

### Resources
Resources are data sources that LLMs can read:
- Identified by URI strings
- Can be text, binary data, or subresources
- Accessed via `resources/read` method
- Listed via `resources/list` method

### Prompts
Prompt templates help LLMs generate consistent outputs:
- Defined with name, description, and arguments
- Retrieved via `prompts/get` method
- Listed via `prompts/list` method

## Standard MCP Methods

### Core Methods (Required for basic functionality)
| Method | Description |
|--------|-------------|
| `initialize` | First handshake - exchanges server/client info and negotiates capabilities |
| `tools/list` | Lists available tools with their input schemas |
| `tools/call` | Invokes a specific tool with provided arguments |
| `notifications/` | Server-sent notifications (progress, logging, etc.) |

### Resource Methods
| Method | Description |
|--------|-------------|
| `resources/list` | Lists available resources |
| `resources/read` | Reads a specific resource by URI |
| `resources/subscribe` | Subscribes to resource changes (advanced) |
| `resources/unsubscribe` | Unsubscribes from resource changes |

### Prompt Methods
| Method | Description |
|--------|-------------|
| `prompts/list` | Lists available prompt templates |
| `prompts/get` | Retrieves a specific prompt template with arguments |

## Error Handling
MCP uses JSON-RPC 2.0 error objects:
- Standard error codes: -32700 (parse error), -32600 (invalid request), -32601 (method not found), -32602 (invalid params), -32603 (internal error)
- Custom errors can be defined in the `-32000` to `-32099` range
- Errors include optional `data` field for additional context

## Server Lifecycle
1. **Initialization**: Server receives `initialize` request, responds with server info and capabilities
2. **Operation**: Server processes incoming requests (tool calls, resource reads, etc.)
3. **Notifications**: Server may send unsolicited notifications (logging, progress)
4. **Termination**: Server ends when stdio closes or receives shutdown signal

## Implementation Approaches

### SDK-Based Servers
- Use official language-specific MCP SDKs
- Provide abstractions for server creation, tool registration, and transport handling
- Handle JSON-RPC messaging and error formatting automatically
- Examples: `python_sdk_server`, `java_sdk_server`, `csharp_sdk_server`, `rust_sdk_server`

### Pure JSON-RPC Servers
- Implement MCP protocol manually using JSON-RPC 2.0 directly
- Offer full control over the protocol implementation
- Useful for learning or environments where SDKs aren't available
- Examples: `pure_jsonrpc_python_server`, `pure_java_server`, `pure_csharp_server`

## Security Considerations
- Servers should validate all inputs according to their JSON Schemas
- Implement proper error handling to avoid information leakage
- Consider sandboxing for tools that execute arbitrary code
- Be mindful of resource exposure - only share intended data
- Authentication is typically handled at the transport level (if needed)

## Extensibility
- Servers can define custom methods beyond the MCP standard
- Capabilities negotiation allows clients to adapt to server features
- New MCP versions can introduce additional methods while maintaining backward compatibility

## Best Practices
1. Keep tool implementations focused and idempotent when possible
2. Provide clear, descriptive documentation in tool/resource/prompt definitions
3. Handle edge cases gracefully (missing arguments, invalid types, etc.)
4. Use appropriate content types (text vs image vs embedded resources)
5. Log appropriately for debugging without exposing sensitive information
6. Follow the principle of least privilege - only expose what's necessary