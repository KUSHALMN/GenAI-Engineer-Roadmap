"""Tool Dispatcher routing LLM tool calls to registered handlers."""
from typing import Dict, Any, Callable
from .tool_executor import ToolExecutor


class ToolDispatcher:
    """Dispatches tool calls with argument validation and error handling."""

    def __init__(self):
        self.registry: Dict[str, Callable] = {
            "calculate_mortgage": ToolExecutor.calculate_mortgage,
            "lookup_stock_ticker": ToolExecutor.lookup_stock_ticker,
        }

    def dispatch(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch a single function call with safe execution."""
        if tool_name not in self.registry:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not recognized in dispatcher registry."
            }

        func = self.registry[tool_name]
        try:
            result = func(**arguments)
            return {"success": True, "tool": tool_name, "output": result}
        except TypeError as e:
            return {"success": False, "tool": tool_name, "error": f"Argument signature mismatch: {str(e)}"}
        except Exception as e:
            return {"success": False, "tool": tool_name, "error": f"Execution error: {str(e)}"}
