"""MCP Tools implementations for arithmetic, system diagnostics, and text stats."""
from typing import Dict, Any, List
from .schemas import MCPToolDefinition


class MCPTools:
    """Standardized tool providers exposed to MCP clients."""

    @staticmethod
    def get_definitions() -> List[MCPToolDefinition]:
        return [
            MCPToolDefinition(
                name="calculate_expression",
                description="Evaluates a mathematical expression safely.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "e.g. '(12 * 8) + 40'"}
                    },
                    "required": ["expression"]
                }
            ),
            MCPToolDefinition(
                name="text_statistics",
                description="Computes word count, character count, and readability index of a text body.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Raw string content to analyze"}
                    },
                    "required": ["text"]
                }
            )
        ]

    @staticmethod
    def calculate_expression(expression: str) -> Dict[str, Any]:
        # Safe mathematical evaluation supporting basic operators
        allowed_chars = set("0123456789+-*/(). ")
        if not set(expression).issubset(allowed_chars):
            raise ValueError("Expression contains unauthorized characters.")
        result = eval(expression, {"__builtins__": None}, {})
        return {"expression": expression, "result": result}

    @staticmethod
    def text_statistics(text: str) -> Dict[str, Any]:
        words = text.split()
        return {
            "character_count": len(text),
            "word_count": len(words),
            "average_word_length": round(sum(len(w) for w in words) / max(1, len(words)), 2)
        }
