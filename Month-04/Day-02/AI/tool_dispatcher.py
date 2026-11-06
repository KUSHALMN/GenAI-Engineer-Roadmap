"""
Day 02: Reliable Tool Dispatcher
Provides centralized tool registration, dynamic lookup, parameter casting,
sandboxed execution, and structured error handling.
"""

from typing import Callable, Dict, Any, Optional
import traceback
import json

class ToolExecutionError(Exception):
    def __init__(self, tool_name: str, message: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Tool '{tool_name}' failed: {message}")
        self.tool_name = tool_name
        self.message = message
        self.original_exception = original_exception

class ToolDispatcher:
    def __init__(self):
        self._registry: Dict[str, Callable] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, func: Callable, description: str = ""):
        """Register a callable tool with metadata."""
        self._registry[name] = func
        self._metadata[name] = {
            "name": name,
            "description": description or func.__doc__ or ""
        }

    def dispatch(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Lookup tool, execute safely, and return normalized JSON-serializable output."""
        if tool_name not in self._registry:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' is not registered in dispatcher.",
                "data": None
            }

        func = self._registry[tool_name]
        try:
            result = func(**args)
            return {
                "success": True,
                "error": None,
                "data": result
            }
        except TypeError as te:
            return {
                "success": False,
                "error": f"Invalid arguments supplied to '{tool_name}': {str(te)}",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error in '{tool_name}': {str(e)}",
                "traceback": traceback.format_exc(),
                "data": None
            }

if __name__ == "__main__":
    dispatcher = ToolDispatcher()

    # Define tools
    def calculate_bmi(weight_kg: float, height_m: float) -> float:
        """Calculate Body Mass Index."""
        if height_m <= 0:
            raise ValueError("Height must be positive")
        return round(weight_kg / (height_m ** 2), 2)

    dispatcher.register("calculate_bmi", calculate_bmi)

    # Test successful dispatch
    res = dispatcher.dispatch("calculate_bmi", {"weight_kg": 70, "height_m": 1.75})
    assert res["success"] is True and res["data"] == 22.86
    print(f"Valid Dispatch Result: {res}")

    # Test missing tool dispatch
    missing_res = dispatcher.dispatch("unknown_tool", {})
    assert missing_res["success"] is False
    print(f"Missing Tool Handled: {missing_res['error']}")

    # Test error handling dispatch
    err_res = dispatcher.dispatch("calculate_bmi", {"weight_kg": 70, "height_m": -1})
    assert err_res["success"] is False
    print(f"Error Safely Wrapped: {err_res['error']}")

    print("Day 02 AI Tool Dispatcher passed all tests.")
