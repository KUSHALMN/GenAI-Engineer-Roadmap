"""Model Context Protocol (MCP) Server implementing JSON-RPC 2.0 dispatch."""
import json
from typing import Dict, Any, Optional
from .schemas import JSONRPCRequest, JSONRPCResponse
from .tools import MCPTools
from .resources import MCPResourceManager


class MCPServer:
    """Server responding to MCP specification methods: tools/list, tools/call, resources/list, resources/read."""

    def __init__(self, server_name: str = "production-mcp-server"):
        self.server_name = server_name
        self.resource_manager = MCPResourceManager()

    def handle_request(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request_payload.get("id", "1")
        method = request_payload.get("method", "")
        params = request_payload.get("params", {})

        try:
            if method == "tools/list":
                defs = [t.to_dict() for t in MCPTools.get_definitions()]
                return JSONRPCResponse(id=req_id, result={"tools": defs}).to_dict()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if tool_name == "calculate_expression":
                    res = MCPTools.calculate_expression(**arguments)
                elif tool_name == "text_statistics":
                    res = MCPTools.text_statistics(**arguments)
                else:
                    return JSONRPCResponse(
                        id=req_id,
                        error={"code": -32601, "message": f"Method/Tool '{tool_name}' not found"}
                    ).to_dict()
                return JSONRPCResponse(id=req_id, result={"content": res}).to_dict()

            elif method == "resources/list":
                res_defs = [r.to_dict() for r in self.resource_manager.list_resources()]
                return JSONRPCResponse(id=req_id, result={"resources": res_defs}).to_dict()

            elif method == "resources/read":
                uri = params.get("uri")
                content = self.resource_manager.read_resource(uri)
                if content is None:
                    return JSONRPCResponse(
                        id=req_id,
                        error={"code": -32002, "message": f"Resource URI '{uri}' not found"}
                    ).to_dict()
                return JSONRPCResponse(id=req_id, result={"contents": [{"uri": uri, "text": content}]}).to_dict()

            else:
                return JSONRPCResponse(
                    id=req_id,
                    error={"code": -32601, "message": f"Unknown JSON-RPC method: {method}"}
                ).to_dict()

        except Exception as e:
            return JSONRPCResponse(
                id=req_id,
                error={"code": -32000, "message": f"Internal execution error: {str(e)}"}
            ).to_dict()
