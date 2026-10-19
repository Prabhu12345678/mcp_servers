#!/usr/bin/env python3
"""
Test script for MCP servers.
Launches the server as a subprocess and sends JSON-RPC requests to verify:
  - initialize
  - tools/list
  - tools/call (for the 'add' tool)
"""

import subprocess
import json
import sys
import argparse

def send_request(proc, request):
    """Send a JSON-RPC request and read one response line."""
    # Write request
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    # Read response
    line = proc.stdout.readline()
    if not line:
        raise Exception("Server closed output")
    return json.loads(line)

def test_server(server_command):
    """Launch server and run tests."""
    # Start the server process
    # We use stdin/stdout pipes and buffer line by line
    proc = subprocess.Popen(
        server_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Use text mode for stdin/stdout
        shell=True  # Allow shell command (so we can use python src/... etc.)
    )

    try:
        # 1. Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        init_response = send_request(proc, init_request)
        if "error" in init_response:
            raise Exception(f"Initialize error: {init_response['error']}")
        # Check that we got a result with serverInfo
        if "result" not in init_response:
            raise Exception("Initialize missing result")
        print("✓ Initialize passed")

        # 2. Tools list
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        list_response = send_request(proc, list_request)
        if "error" in list_response:
            raise Exception(f"Tools/list error: {list_response['error']}")
        if "result" not in list_response:
            raise Exception("Tools/list missing result")
        tools = list_response["result"].get("tools", [])
        if not any(tool.get("name") == "add" for tool in tools):
            raise Exception("Tools list does not contain 'add' tool")
        print("✓ Tools/list passed")

        # 3. Tools call for add
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {
                    "a": 1,
                    "b": 2
                }
            }
        }
        call_response = send_request(proc, call_request)
        if "error" in call_response:
            raise Exception(f"Tools/call error: {call_response['error']}")
        if "result" not in call_response:
            raise Exception("Tools/call missing result")
        # Extract the text content
        content = call_response["result"].get("content", [])
        if not content or content[0].get("type") != "text":
            raise Exception("Unexpected content type in add tool result")
        result_text = content[0].get("text", "")
        if "3" not in result_text:
            raise Exception(f"Expected result to contain '3', got: {result_text}")
        print("✓ Tools/call (add) passed")

        print("\nAll tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        # Print stderr for debugging
        stderr_output = proc.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")
        sys.exit(1)
    finally:
        # Terminate the server
        proc.terminate()
        proc.wait(timeout=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test an MCP server.")
    parser.add_argument(
        "--command",
        required=True,
        help="Command to launch the server (e.g., 'python src/mcp_add_server.py')"
    )
    args = parser.parse_args()
    test_server(args.command)