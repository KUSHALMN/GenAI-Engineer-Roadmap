import ast
import operator
import math
from typing import Union

try:
    from schemas import CalculationResult
except ImportError:
    from ..schemas import CalculationResult



class SafeCalculator:
    """
    Evaluates mathematical expressions safely using Abstract Syntax Trees (AST).
    Prevents arbitrary code execution and injection vulnerabilities.
    """

    ALLOWED_OPERATORS = {
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

    ALLOWED_FUNCTIONS = {
        "sqrt": math.sqrt,
        "log": math.log,
        "log2": math.log2,
        "log10": math.log10,
        "exp": math.exp,
        "ceil": math.ceil,
        "floor": math.floor,
        "round": round,
        "abs": abs,
        "pow": pow,
        "min": min,
        "max": max,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
    }

    ALLOWED_CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "GB": 1024 ** 3,
        "MB": 1024 ** 2,
        "KB": 1024,
        "BILLION": 1_000_000_000,
        "MILLION": 1_000_000,
    }

    def _eval(self, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.Name):
            if node.id in self.ALLOWED_CONSTANTS:
                return self.ALLOWED_CONSTANTS[node.id]
            raise ValueError(f"Unknown variable or identifier: '{node.id}'")

        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in self.ALLOWED_FUNCTIONS:
                func = self.ALLOWED_FUNCTIONS[node.func.id]
                args = [self._eval(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Unsupported function call: '{getattr(node.func, 'id', str(node.func))}'")

        else:
            raise ValueError(f"Unsupported AST node expression: {type(node).__name__}")

    def evaluate(self, expression: str) -> CalculationResult:
        """
        Safely evaluates mathematical string and formats results.
        """
        clean_expr = expression.strip()
        try:
            parsed = ast.parse(clean_expr, mode="eval")
            val = self._eval(parsed.body)
            float_val = float(val)

            # Human-friendly formatting
            if abs(float_val) >= 1_000_000_000:
                formatted = f"{float_val:,.4f} ({float_val / 1e9:.2f} Billion / {float_val:.2e})"
            elif abs(float_val) >= 1_000_000:
                formatted = f"{float_val:,.4f} ({float_val / 1e6:.2f} Million)"
            elif float_val.is_integer():
                formatted = f"{int(float_val):,}"
            else:
                formatted = f"{float_val:.6f}".rstrip("0").rstrip(".")

            return CalculationResult(
                expression=clean_expr,
                result=float_val,
                formatted=formatted,
                success=True,
                error=None
            )
        except Exception as e:
            return CalculationResult(
                expression=clean_expr,
                result=0.0,
                formatted="ERROR",
                success=False,
                error=str(e)
            )


# Global singleton instance
_calculator = SafeCalculator()


def calculate(expression: str) -> CalculationResult:
    """Module-level function exposed to tools registry."""
    return _calculator.evaluate(expression)
