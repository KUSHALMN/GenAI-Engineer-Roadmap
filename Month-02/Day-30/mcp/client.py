"""Model Context Protocol (MCP) Client for interacting with MCP Servers."""
from typing import Dict, Any, List
from .server import MCPServer
from .schemas import JSONRPCRequest


class MCPClient:
    """Client issuing standard JSON-RPC 2.0 calls to MCP Servers."""

    def __init__(self, server: MCPServer):
        self.server = server
        self._request_counter = 0

    def _next_id(self) -> str:
        self._request_counter += 1
        return str(self._request_counter)

    def list_tools(self) -> List[Dict[str, Any]]:
        req = JSONRPCRequest(id=self._next_id(), method="tools/list").to_dict()
        resp = self.server.handle_request(req)
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        req = JSONRPCRequest(
            id=self._next_id(),
            method="tools/call",
            params={"name": name, "arguments": arguments}
        ).to_dict()
        resp = self.server.handle_request(req)
        if resp.get("error"):
            raise RuntimeError(f"MCP Tool Error: {resp['error']['message']}")
        return resp.get("result", {}).get("content", {})

    def list_resources(self) -> List[Dict[str, Any]]:
        req = JSONRPCRequest(id=self._next_id(), method="resources/list").to_dict()
        resp = self.server.handle_request(req)
        return resp.get("result", {}).get("resources", [])

    def read_resource(self, uri: str) -> str:
        req = JSONRPCRequest(
            id=self._next_id(),
            method="resources/read",
            params={"uri": uri}
        ).to_dict()
        resp = self.server.handle_request(req)
        if resp.get("error"):
            raise RuntimeError(f"MCP Resource Error: {resp['error']['message']}")
        return resp.get("result", {}).get("contents", [{}])[0].get("text", "")
