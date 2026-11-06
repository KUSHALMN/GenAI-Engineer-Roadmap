"""
Day 15: MCP Protocol Fundamentals
Validates Model Context Protocol (MCP) JSON-RPC 2.0 messages,
handles lifecycle handshakes (initialize/initialized), and capability exchanges.
"""

from typing import Dict, Any, Optional
import json

class MCPProtocolValidator:
    @staticmethod
    def validate_jsonrpc_message(msg: Dict[str, Any]) -> bool:
        """Ensures JSON-RPC 2.0 conformance."""
        if msg.get("jsonrpc") != "2.0":
            return False
        if "id" not in msg and "method" not in msg:
            return False
        return True

    @staticmethod
    def build_initialize_request(client_name: str, version: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": False}
                },
                "clientInfo": {"name": client_name, "version": version}
            }
        }

    @staticmethod
    def build_initialize_response(request_id: int, server_name: str, server_version: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "serverInfo": {"name": server_name, "version": server_version}
            }
        }

if __name__ == "__main__":
    val = MCPProtocolValidator()
    init_req = val.build_initialize_request("EnterpriseAgentClient", "1.0.0")
    assert val.validate_jsonrpc_message(init_req) is True

    init_resp = val.build_initialize_response(1, "PostgresMCPServer", "2.1.0")
    assert val.validate_jsonrpc_message(init_resp) is True
    assert init_resp["result"]["serverInfo"]["name"] == "PostgresMCPServer"

    print("MCP Protocol Handshake Message Specs:")
    print(json.dumps(init_resp, indent=2))
    print("Day 15 AI MCP Protocol Validator passed all tests.")
