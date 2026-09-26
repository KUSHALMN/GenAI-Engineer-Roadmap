"""
MCP Client.
Discovers tools, validates inputs, and coordinates tool execution via JSON-RPC 2.0.
"""

import json
from typing import Any, Dict, List, Optional
from mcp_server import MCPServer


class MCPClient:
    """Client for interacting with MCP servers."""

    def __init__(self, server: MCPServer, client_role: str = "user"):
        self.server = server
        self.client_role = client_role
        self._request_counter = 0
        self.discovered_tools: Dict[str, Dict[str, Any]] = {}

    def _next_id(self) -> int:
        self._request_counter += 1
        return self._request_counter

    def discover_tools(self) -> List[Dict[str, Any]]:
        """Call 'tools/list' on the MCP server and cache schemas."""
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {},
        }
        res = self.server.handle_request(req, user_role=self.client_role)
        if "error" in res:
            raise RuntimeError(f"Failed to discover tools: {res['error']}")

        tools = res.get("result", {}).get("tools", [])
        self.discovered_tools = {t["name"]: t for t in tools}
        return tools

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool by name with arguments."""
        if tool_name not in self.discovered_tools:
            # Refresh list
            self.discover_tools()
            if tool_name not in self.discovered_tools:
                raise ValueError(f"Tool '{tool_name}' not available on server")

        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        res = self.server.handle_request(req, user_role=self.client_role)
        if "error" in res:
            raise RuntimeError(f"MCP Call Error: {res['error']['message']}")

        content = res.get("result", {}).get("content", [])
        if content and content[0].get("type") == "text":
            return json.loads(content[0]["text"])

        return content


if __name__ == "__main__":
    server = MCPServer()
    client = MCPClient(server)

    # 1. Discover tools
    tools = client.discover_tools()
    print("Discovered Tools:", [t["name"] for t in tools])
    assert len(tools) >= 2

    # 2. Call evaluate_expression
    calc_res = client.call_tool("evaluate_expression", {"a": 100, "b": 25, "operator": "/"})
    print("Calc Result:", calc_res)
    assert calc_res["result"] == 4.0

    # 3. Call system metrics
    metrics = client.call_tool("get_system_metrics", {})
    print("System Metrics:", metrics["os"], metrics["architecture"])
    assert "cpu_count" in metrics

    print("MCP Client tests passed successfully!")
