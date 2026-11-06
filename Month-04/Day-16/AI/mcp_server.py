"""
Day 16: Build a Basic MCP Server
Implements a self-contained Model Context Protocol server exposing
tools with JSON schema definitions and handling JSON-RPC 2.0 requests.
"""

from typing import Dict, Any, List
import json

class BasicMCPServer:
    def __init__(self, name: str = "DemoMCPServer"):
        self.name = name
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, input_schema: Dict[str, Any], handler):
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "handler": handler
        }

    def handle_request(self, request_json: str) -> str:
        req = json.loads(request_json)
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": self.name, "version": "1.0.0"}
                }
            })
        elif method == "tools/list":
            tool_list = [
                {"name": t["name"], "description": t["description"], "inputSchema": t["inputSchema"]}
                for t in self.tools.values()
            ]
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": tool_list}
            })
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name not in self.tools:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })
            try:
                res = self.tools[tool_name]["handler"](**args)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": str(res)}]}
                })
            except Exception as e:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                })

        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not implemented"}
        })

if __name__ == "__main__":
    server = BasicMCPServer()

    # Register tools
    server.register_tool(
        "calculate_tax",
        "Calculates sales tax for a given amount and rate.",
        {"type": "object", "properties": {"amount": {"type": "number"}, "rate": {"type": "number"}}, "required": ["amount", "rate"]},
        lambda amount, rate: round(amount * rate, 2)
    )

    # 1. Initialize
    init_res = json.loads(server.handle_request(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert init_res["result"]["serverInfo"]["name"] == "DemoMCPServer"

    # 2. Tools list
    list_res = json.loads(server.handle_request(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 1

    # 3. Call tool
    call_res = json.loads(server.handle_request(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "calculate_tax", "arguments": {"amount": 100, "rate": 0.08}}
    })))
    assert call_res["result"]["content"][0]["text"] == "8.0"
    print("MCP Server response for tool call:")
    print(call_res)
    print("Day 16 AI Basic MCP Server passed all tests.")
