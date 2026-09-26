"""
Tool Schema Generator.
Converts Python callable signatures and type hints into standard JSON Schema specifications
compatible with OpenAI, Anthropic, and Groq function-calling protocols.
"""

import inspect
from typing import Any, Callable, Dict, get_type_hints


def python_type_to_json_schema(py_type: Any) -> Dict[str, Any]:
    """Map python types to JSON Schema types."""
    if py_type == str:
        return {"type": "string"}
    elif py_type == int:
        return {"type": "integer"}
    elif py_type == float:
        return {"type": "number"}
    elif py_type == bool:
        return {"type": "boolean"}
    elif py_type == list or getattr(py_type, "__origin__", None) == list:
        return {"type": "array", "items": {"type": "string"}}
    elif py_type == dict or getattr(py_type, "__origin__", None) == dict:
        return {"type": "object"}
    return {"type": "string"}


def generate_tool_schema(func: Callable) -> Dict[str, Any]:
    """Generates standard OpenAI function call definition from Python function."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or f"Execute {func.__name__}"
    type_hints = get_type_hints(func)

    properties: Dict[str, Any] = {}
    required: list[str] = []

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        param_type = type_hints.get(param_name, str)
        schema_type = python_type_to_json_schema(param_type)
        properties[param_name] = schema_type

        # Check if parameter has no default value
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\n\n")[0],
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


if __name__ == "__main__":
    def query_database(sql: str, max_rows: int = 100) -> list:
        """Execute a read-only SQL query against the warehouse."""
        return []

    schema = generate_tool_schema(query_database)
    print("Generated Schema:", schema)
    assert schema["function"]["name"] == "query_database"
    assert "sql" in schema["function"]["parameters"]["properties"]
    assert "sql" in schema["function"]["parameters"]["required"]
    assert "max_rows" not in schema["function"]["parameters"]["required"]
    print("Tool schema generation passed successfully!")
