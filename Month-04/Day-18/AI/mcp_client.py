"""
Day 18: Build an MCP Client
Connects to an MCP server, initiates capability handshakes,
discovers registered tools, and executes calls over simulated JSON-RPC communication.
"""

from typing import Dict, Any, List
import json

class MCPClient:
    def __init__(self, server_target):
        self.server = server_target
        self.connected = False
        self.available_tools: List[Dict[str, Any]] = []

    def connect(self) -> bool:
        """Executes initialize handshake."""
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"clientInfo": {"name": "AgentHostClient", "version": "1.0"}}
        }
        res_str = self.server.handle_request(json.dumps(init_req))
        res = json.loads(res_str)
        if "result" in res:
            self.connected = True
            self._fetch_tools()
            return True
        return False

    def _fetch_tools(self):
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        res = json.loads(self.server.handle_request(json.dumps(list_req)))
        self.available_tools = res.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.connected:
            raise ConnectionError("Client is not connected to MCP Server.")
        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments}
        }
        res = json.loads(self.server.handle_request(json.dumps(call_req)))
        if "error" in res:
            raise RuntimeError(f"MCP Error: {res['error']['message']}")
        return res["result"]["content"][0]["text"]

if __name__ == "__main__":
    # Mock server
    class MockServer:
        def handle_request(self, s):
            req = json.loads(s)
            if req["method"] == "initialize":
                return json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {"serverInfo": {"name": "TestServer"}}})
            elif req["method"] == "tools/list":
                return json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {"tools": [{"name": "echo", "description": "echoes text"}]}})
            elif req["method"] == "tools/call":
                return json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {"content": [{"type": "text", "text": req["params"]["arguments"]["text"]}]}})
            return json.dumps({"error": "unknown"})

    client = MCPClient(MockServer())
    assert client.connect() is True
    assert len(client.available_tools) == 1
    
    echo_res = client.call_tool("echo", {"text": "Hello MCP!"})
    assert echo_res == "Hello MCP!"
    print(f"MCP Client successfully invoked tool: '{echo_res}'")
    print("Day 18 AI MCP Client passed all tests.")
