"""
Minimal MCP (Model Context Protocol) Server.
Implements JSON-RPC 2.0 protocol for tool discovery and execution.
Supported Methods:
- "tools/list": Returns metadata and JSON schemas for available tools
- "tools/call": Validates permissions and executes tool
"""

import json
import sys
from typing import Any, Dict, List, Optional
from tools.calculator import evaluate_expression, get_tool_definition as get_calc_def
from tools.system_metrics import get_system_metrics, get_tool_definition as get_metrics_def


class MCPServer:
    """JSON-RPC 2.0 MCP Tool Server."""

    def __init__(self, allowed_roles: Optional[List[str]] = None):
        self.allowed_roles = allowed_roles or ["user", "admin"]
        self.tools = {
            "get_system_metrics": {
                "handler": get_system_metrics,
                "def": get_metrics_def(),
                "requires_role": "user",
            },
            "evaluate_expression": {
                "handler": evaluate_expression,
                "def": get_calc_def(),
                "requires_role": "user",
            },
        }

    def handle_request(self, json_rpc_payload: Dict[str, Any], user_role: str = "user") -> Dict[str, Any]:
        """Process incoming JSON-RPC request."""
        req_id = json_rpc_payload.get("id")
        method = json_rpc_payload.get("method")
        params = json_rpc_payload.get("params", {})

        # Basic JSON-RPC protocol validation
        if json_rpc_payload.get("jsonrpc") != "2.0" or not method:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: expected jsonrpc 2.0"},
            }

        # Route methods
        if method == "tools/list":
            return self._handle_tools_list(req_id)
        elif method == "tools/call":
            return self._handle_tools_call(req_id, params, user_role)
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    def _handle_tools_list(self, req_id: Any) -> Dict[str, Any]:
        """List all available tools."""
        tool_list = [t["def"] for t in self.tools.values()]
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": tool_list},
        }

    def _handle_tools_call(self, req_id: Any, params: Dict[str, Any], user_role: str) -> Dict[str, Any]:
        """Validate permissions, arguments, and invoke tool."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name or tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Unknown tool: '{tool_name}'"},
            }

        tool_meta = self.tools[tool_name]

        # Permission check
        if user_role not in self.allowed_roles:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": f"Permission denied for role '{user_role}'"},
            }

        # Execute handler
        try:
            handler = tool_meta["handler"]
            output = handler(**arguments) if arguments else handler()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(output)}]},
            }
        except TypeError as te:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Invalid arguments: {te}"},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32001, "message": f"Tool execution failed: {e}"},
            }


if __name__ == "__main__":
    server = MCPServer()

    # Test tools/list
    list_req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    list_res = server.handle_request(list_req)
    assert len(list_res["result"]["tools"]) == 2

    # Test tools/call
    call_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "evaluate_expression",
            "arguments": {"a": 12.0, "b": 4.0, "operator": "*"},
        },
    }
    call_res = server.handle_request(call_req)
    assert "result" in call_res
    text_content = call_res["result"]["content"][0]["text"]
    assert json.loads(text_content)["result"] == 48.0

    print("MCP Server tests passed successfully!")
