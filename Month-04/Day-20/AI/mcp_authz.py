"""
Day 20: MCP Authentication and Authorization
Enforces fine-grained token authorization and scope permissions for MCP operations:
- Scopes: read:metrics, tools:execute, admin:destructive
"""

from typing import Dict, Any, List, Set

class MCPAuthorizer:
    def __init__(self):
        # Token to scopes mapping
        self.valid_tokens: Dict[str, Set[str]] = {
            "tok_analyst_1": {"read:metrics"},
            "tok_engineer_2": {"read:metrics", "tools:execute"},
            "tok_admin_9": {"read:metrics", "tools:execute", "admin:destructive"}
        }
        # Tool requirement mapping
        self.tool_requirements: Dict[str, str] = {
            "get_metrics": "read:metrics",
            "restart_service": "tools:execute",
            "drop_database": "admin:destructive"
        }

    def authorize_tool_call(self, token: str, tool_name: str) -> Dict[str, Any]:
        if token not in self.valid_tokens:
            return {"authorized": False, "code": 401, "error": "Invalid bearer token."}

        required_scope = self.tool_requirements.get(tool_name)
        if not required_scope:
            return {"authorized": False, "code": 404, "error": f"Tool '{tool_name}' unknown."}

        user_scopes = self.valid_tokens[token]
        if required_scope not in user_scopes:
            return {
                "authorized": False,
                "code": 403,
                "error": f"Forbidden: Action '{tool_name}' requires scope '{required_scope}'."
            }

        return {"authorized": True, "code": 200, "error": None}

if __name__ == "__main__":
    authz = MCPAuthorizer()

    # Analyst attempts metrics (Allowed)
    a1 = authz.authorize_tool_call("tok_analyst_1", "get_metrics")
    assert a1["authorized"] is True

    # Analyst attempts restart (Denied)
    a2 = authz.authorize_tool_call("tok_analyst_1", "restart_service")
    assert a2["authorized"] is False and a2["code"] == 403

    # Admin attempts drop (Allowed)
    a3 = authz.authorize_tool_call("tok_admin_9", "drop_database")
    assert a3["authorized"] is True

    print("Authorization Policy verification passed:")
    print(f"Analyst -> get_metrics: {a1['authorized']}")
    print(f"Analyst -> restart_service: {a2['authorized']} (Code {a2['code']})")
    print(f"Admin   -> drop_database: {a3['authorized']}")
    print("Day 20 AI MCP AuthZ passed all tests.")
