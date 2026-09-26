"""
Safe Calculator Tool for MCP Server.
"""

from typing import Any, Dict


def evaluate_expression(a: float, b: float, operator: str) -> Dict[str, Any]:
    """Execute mathematical computation."""
    if operator == "+":
        res = a + b
    elif operator == "-":
        res = a - b
    elif operator == "*":
        res = a * b
    elif operator == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero is not permitted")
        res = a / b
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    return {"a": a, "b": b, "operator": operator, "result": res}


def get_tool_definition() -> Dict[str, Any]:
    """MCP tool definition schema."""
    return {
        "name": "evaluate_expression",
        "description": "Performs basic arithmetic operations (+, -, *, /).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First operand"},
                "b": {"type": "number", "description": "Second operand"},
                "operator": {"type": "string", "enum": ["+", "-", "*", "/"], "description": "Arithmetic operator"},
            },
            "required": ["a", "b", "operator"],
        },
    }
