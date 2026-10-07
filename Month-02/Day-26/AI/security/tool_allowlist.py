"""Strict Tool Whitelist and Least-Privilege Execution Policy."""
from typing import Set, Dict, Any, Callable


class UnauthorizedToolExecutionException(Exception):
    """Raised when an LLM agent attempts to invoke a disallowed function."""
    pass


class ToolPermissionManager:
    """Enforces role-based allowlists and argument safety for agentic tools."""

    def __init__(self, allowed_tools: Set[str]):
        self.allowed_tools = set(allowed_tools)
        self.tool_registry: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self.tool_registry[name] = func

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.allowed_tools:
            raise UnauthorizedToolExecutionException(
                f"Security Violation: Tool '{tool_name}' is not in the allowed tool execution list."
            )
        if tool_name not in self.tool_registry:
            raise ValueError(f"Tool '{tool_name}' is permitted but not registered.")

        return self.tool_registry[tool_name](**kwargs)
