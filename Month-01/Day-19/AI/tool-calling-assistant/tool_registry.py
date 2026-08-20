"""
Tool Registry for dynamic tool discovery, JSON schema generation, and safe execution.
"""

import inspect
import json
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from schemas import FunctionDefinition, Tool, ToolExecutionResult


class ToolRegistry:
    """Manages available tools, automates schema derivation, and dispatches calls."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, Tool] = {}

    def _python_type_to_json_schema(self, py_type: Any) -> Dict[str, Any]:
        """Maps Python type annotations to JSON Schema types."""
        if py_type in (int, float):
            return {"type": "number" if py_type is float else "integer"}
        elif py_type is str:
            return {"type": "string"}
        elif py_type is bool:
            return {"type": "boolean"}
        elif py_type in (list, List) or getattr(py_type, "__origin__", None) in (list, List):
            return {"type": "array", "items": {"type": "string"}}
        elif py_type in (dict, Dict) or getattr(py_type, "__origin__", None) in (dict, Dict):
            return {"type": "object"}
        return {"type": "string"}

    def register(self, func: Optional[Callable] = None, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator or method to register a callable Python function as an LLM tool."""
        def decorator(fn: Callable) -> Callable:
            tool_name = name or fn.__name__
            doc = description or inspect.getdoc(fn) or "No description provided."

            sig = inspect.signature(fn)
            type_hints = get_type_hints(fn)

            properties: Dict[str, Any] = {}
            required_params: List[str] = []

            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue

                param_type = type_hints.get(param_name, str)
                prop_schema = self._python_type_to_json_schema(param_type)

                # Use parameter doc if available or a basic description
                prop_schema["description"] = f"Parameter '{param_name}'"

                if param.default is inspect.Parameter.empty:
                    required_params.append(param_name)
                else:
                    prop_schema["default"] = param.default

                properties[param_name] = prop_schema

            function_def = FunctionDefinition(
                name=tool_name,
                description=doc.split("\n\n")[0].strip(),
                parameters={
                    "type": "object",
                    "properties": properties,
                    "required": required_params,
                },
            )

            self._tools[tool_name] = fn
            self._schemas[tool_name] = Tool(function=function_def)
            return fn

        if func is not None:
            return decorator(func)
        return decorator

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Returns the list of tool definitions compatible with OpenAI / Groq tool calling API."""
        return [tool.model_dump() for tool in self._schemas.values()]

    def execute(self, tool_call_id: str, function_name: str, arguments_str: str) -> ToolExecutionResult:
        """Executes a registered function with JSON serialized arguments."""
        if function_name not in self._tools:
            return ToolExecutionResult(
                tool_call_id=tool_call_id,
                name=function_name,
                success=False,
                result=None,
                error=f"Tool '{function_name}' is not registered.",
            )

        func = self._tools[function_name]
        try:
            if isinstance(arguments_str, str) and arguments_str.strip():
                kwargs = json.loads(arguments_str)
            elif isinstance(arguments_str, dict):
                kwargs = arguments_str
            else:
                kwargs = {}

            res = func(**kwargs)
            return ToolExecutionResult(
                tool_call_id=tool_call_id,
                name=function_name,
                success=True,
                result=res,
            )
        except json.JSONDecodeError as jde:
            return ToolExecutionResult(
                tool_call_id=tool_call_id,
                name=function_name,
                success=False,
                result=None,
                error=f"Invalid JSON arguments: {jde}",
            )
        except TypeError as te:
            return ToolExecutionResult(
                tool_call_id=tool_call_id,
                name=function_name,
                success=False,
                result=None,
                error=f"Argument mismatch: {te}",
            )
        except Exception as e:
            return ToolExecutionResult(
                tool_call_id=tool_call_id,
                name=function_name,
                success=False,
                result=None,
                error=f"Execution error: {str(e)}",
            )
