"""Tool Permission Matrix & Human-In-The-Loop (HITL) Policy Guard."""
from typing import Dict, Any, List, Set


class ToolPermissionGuard:
    """Classifies tools into Read-Only, Safe-Write, and High-Risk (requiring confirmation)."""

    def __init__(self):
        self.read_only_tools = {"get_weather", "search_kb", "calculator", "get_status"}
        self.safe_write_tools = {"send_notification", "create_draft"}
        self.high_risk_tools = {"delete_database", "execute_sql_dml", "transfer_funds", "deploy_release"}

    def check_permission(self, tool_name: str, user_role: str = "standard_user") -> Dict[str, Any]:
        if tool_name in self.read_only_tools:
            return {"allowed": True, "requires_hitl": False, "reason": "Read-only operation"}

        if tool_name in self.safe_write_tools:
            return {"allowed": True, "requires_hitl": False, "reason": "Standard safe write"}

        if tool_name in self.high_risk_tools:
            if user_role == "admin":
                return {"allowed": True, "requires_hitl": True, "reason": "Admin high-risk HITL approval required"}
            return {"allowed": False, "requires_hitl": False, "reason": "Permission Denied: User role cannot execute destructive tool"}

        return {"allowed": False, "requires_hitl": False, "reason": f"Unknown tool: '{tool_name}'"}
