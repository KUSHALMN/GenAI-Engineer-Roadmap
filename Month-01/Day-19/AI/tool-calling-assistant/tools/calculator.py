"""
Calculator tool for safe mathematical evaluation.
Parses mathematical expressions using AST safely to prevent arbitrary code execution.
"""

import ast
import operator
import math
from typing import Union


SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "abs": abs,
    "round": round,
}

SAFE_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


def _eval_node(node: ast.AST) -> Union[int, float]:
    """Recursively evaluates an AST node in a restricted math environment."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    elif isinstance(node, ast.Name):
        if node.id.lower() in SAFE_CONSTANTS:
            return SAFE_CONSTANTS[node.id.lower()]
        raise ValueError(f"Unknown constant or variable: '{node.id}'")

    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id.lower() in SAFE_FUNCTIONS:
            func = SAFE_FUNCTIONS[node.func.id.lower()]
            args = [_eval_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError(f"Unsupported or disallowed function call: '{getattr(node.func, 'id', 'unknown')}'")

    else:
        raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression safely.

    Args:
        expression: A mathematical string, e.g., '2 * (3 + 4)', 'sqrt(144) + 10^2', or 'sin(pi/2)'.

    Returns:
        The evaluated result as a string or an error explanation.
    """
    try:
        # Pre-process common notation like ^ to **
        normalized_expr = expression.strip().replace("^", "**")
        parsed = ast.parse(normalized_expr, mode="eval")
        result = _eval_node(parsed.body)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero is undefined."
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
