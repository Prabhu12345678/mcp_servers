#!/usr/bin/env python3
"""
Pure JSON‑RPC 2.0 MCP server (stdio transport).

Implements only the three core MCP methods:
  - initialize
  - tools/list
  - tools/call   (only the "add" tool)
"""

import json
import sys
from typing import Any, Dict, List

def send_message(msg: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def tool_add(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    a = float(args.get("a", 0))
    b = float(args.get("b", 0))
    result = a + b
    return [
        {
            "type": "text",
            "text": f"The sum of {a} and {b} is {result}."
        }
    ]

def main() -> None:
    server_info = {
        "protocolVersion": "2024-11-05",
        "serverInfo": {
            "name": "pure-jsonrpc-mcp-server",
            "version": "0.1.0"
        },
        "capabilities": {
            "tools": {}
        }
    }

    TOOLS = [
        {
            "name": "add",
            "description": "Return the sum of two numbers.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First addend"},
                    "b": {"type": "number", "description": "Second addend"}
                },
                "required": ["a", "b"]
            }
        }
    ]

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as e:
            send_message({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error",
                    "data": str(e)
                }
            })
            continue

        if request.get("jsonrpc") != "2.0":
            send_message({
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": "Missing or incorrect jsonrpc version"
                }
            })
            continue

        msg_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        response = {"jsonrpc": "2.0", "id": msg_id}

        try:
            if method == "initialize":
                result = server_info
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if tool_name == "add":
                    result = {"content": tool_add(arguments)}
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")
            else:
                raise ValueError(f"Method not found: {method}")
            response["result"] = result
        except Exception as exc:
            # Determine error code
            if isinstance(exc, ValueError) and str(exc).startswith("Unknown tool"):
                code = -32602  # Invalid params
            elif isinstance(exc, ValueError) and str(exc).startswith("Method not found"):
                code = -32601  # Method not found
            else:
                code = -32603  # Internal error
            response["error"] = {
                "code": code,
                "message": str(exc),
                "data": None
            }

        send_message(response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)