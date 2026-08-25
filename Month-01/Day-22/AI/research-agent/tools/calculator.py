"""
Calculator Tool
Provides a secure Abstract Syntax Tree (AST) evaluator for mathematical and
computational formulas (FLOPs, scaling laws, activated parameter ratios).
Avoids unsafe Python eval() execution.
"""

import ast
import operator
import math
from typing import Dict, Any, Union


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

SAFE_NAMES = {
    "pi": math.pi,
    "e": math.e,
    "sqrt": math.sqrt,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "round": round,
    "abs": abs,
}


def _eval_ast_node(node: ast.AST) -> Union[int, float]:
    """Recursively evaluates safe AST nodes without executing arbitrary bytecode."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    elif isinstance(node, ast.Name):
        if node.id in SAFE_NAMES:
            return SAFE_NAMES[node.id]
        raise ValueError(f"Undefined variable or constant: '{node.id}'")

    elif isinstance(node, ast.BinOp):
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            if op_type == ast.Pow and (right > 100 or left > 1e12):
                raise ValueError("Exponentiation values exceed safety thresholds")
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast_node(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_NAMES:
            func = SAFE_NAMES[node.func.id]
            args = [_eval_ast_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError(f"Unsafe or disallowed function call: '{getattr(node.func, 'id', 'unknown')}'")

    else:
        raise ValueError(f"Disallowed syntax construct: {type(node).__name__}")


def evaluate_expression(expression: str) -> Dict[str, Any]:
    """
    Safely parses and evaluates a mathematical string expression via AST.
    
    Args:
        expression (str): Mathematical expression (e.g. '37 / 671 * 100', '6 * (70 * 10**9) * (15 * 10**12)')
        
    Returns:
        Dict[str, Any]: Calculation outcome with numeric value and status.
    """
    clean_expr = expression.strip()
    try:
        parsed_tree = ast.parse(clean_expr, mode='eval')
        numeric_result = _eval_ast_node(parsed_tree.body)
        
        if isinstance(numeric_result, float):
            formatted_value = round(numeric_result, 6)
        else:
            formatted_value = numeric_result

        return {
            "success": True,
            "expression": clean_expr,
            "result": formatted_value,
            "scientific_notation": f"{numeric_result:.4e}" if abs(numeric_result) >= 1e6 or (0 < abs(numeric_result) < 1e-4) else str(formatted_value),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "expression": clean_expr,
            "result": None,
            "scientific_notation": None,
            "error": f"Evaluation error: {str(e)}"
        }
