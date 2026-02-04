import sys
import json
import logging
from typing import Any, Dict, Optional

# Configure logging to stderr so it doesn't interfere with stdout (used for MCP)
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main loop for the MCP server.
    Reads JSON-RPC requests from stdin and writes responses to stdout.
    """
    # logging.info("Starting Hello MCP Server (Python)...")
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            logging.error(f"Error unmarshaling request: {e}")
            continue

        # Basic validation
        if not isinstance(req, dict):
            continue

        req_id = req.get('id')
        method = req.get('method')
        params = req.get('params')

        if method == "initialize":
            handle_initialize(req_id)
        elif method == "tools/list":
            handle_tools_list(req_id)
        elif method == "tools/call":
            handle_tool_call(req_id, params)
        elif method == "notifications/initialized":
            # Client notification that initialization is complete
            pass
        else:
            # Only send error if it's a request (has id), not a notification
            if req_id is not None:
                send_error(req_id, -32601, "Method not found")

def handle_initialize(req_id: Any):
    """
    Handles the 'initialize' method.
    """
    result = {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "hello-server",
            "version": "1.0.0"
        }
    }
    send_result(req_id, result)

def handle_tools_list(req_id: Any):
    """
    Handles the 'tools/list' method.
    """
    result = {
        "tools": [
            {
                "name": "greet",
                "description": "A simple tool that returns a greeting.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the person to greet."
                        }
                    },
                    "required": ["name"]
                }
            }
        ]
    }
    send_result(req_id, result)

def handle_tool_call(req_id: Any, params: Optional[Dict[str, Any]]):
    """
    Handles the 'tools/call' method.
    """
    if not params:
        send_error(req_id, -32602, "Invalid params")
        return

    tool_name = params.get("name")
    if tool_name != "greet":
        send_error(req_id, -32601, "Tool not found")
        return

    tool_arguments = params.get("arguments", {})
    if not isinstance(tool_arguments, dict):
         # Handle case where arguments might be missing or invalid
         tool_arguments = {}

    name = tool_arguments.get("name")
    
    # Emulate Go's behavior: if name is not a string or missing, it becomes empty string
    if not isinstance(name, str):
        name = ""

    greeting = f"Hello, {name}! Welcome to the world of MCP in Python."
    
    result = {
        "content": [
            {
                "type": "text",
                "text": greeting
            }
        ]
    }
    send_result(req_id, result)

def send_result(req_id: Any, result: Any):
    """
    Sends a successful JSON-RPC response.
    """
    response = {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    }
    send_json(response)

def send_error(req_id: Any, code: int, message: str):
    """
    Sends a JSON-RPC error response.
    """
    response = {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    send_json(response)

def send_json(data: Any):
    """
    Encodes data as JSON and writes it to stdout with a trailing newline.
    """
    try:
        json_str = json.dumps(data)
        sys.stdout.write(json_str + "\n")
        sys.stdout.flush()
    except Exception as e:
        logging.error(f"Error marshaling response: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
