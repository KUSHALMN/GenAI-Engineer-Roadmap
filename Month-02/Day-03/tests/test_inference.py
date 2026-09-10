"""
test_inference.py — Unit tests for tools and agent inference logic.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import ast
import operator
import pytest
from schemas import AgentResponse, SearchInput, CalculatorInput, WeatherInput


# ── Tool unit tests (no LLM call needed) ──────────────────────────────────────

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def safe_eval(expression: str):
    tree = ast.parse(expression, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.n
        if isinstance(node, ast.BinOp):
            return SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return SAFE_OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"Unsupported: {node}")

    return _eval(tree.body)


def test_calculator_basic():
    assert safe_eval("2 + 3") == 5
    assert safe_eval("10 * 4") == 40
    assert safe_eval("100 / 4") == 25.0


def test_calculator_complex():
    assert safe_eval("15 * 24 + 100") == 460
    assert safe_eval("2 ** 10") == 1024


def test_calculator_negative():
    assert safe_eval("-5 + 10") == 5


def test_search_input_schema():
    s = SearchInput(query="LangChain agents", max_results=5)
    assert s.query == "LangChain agents"
    assert s.max_results == 5


def test_search_input_defaults():
    s = SearchInput(query="test")
    assert s.max_results == 3


def test_weather_input_schema():
    w = WeatherInput(city="Bangalore")
    assert w.city == "Bangalore"
    assert w.units == "celsius"


def test_weather_input_units_validation():
    with pytest.raises(Exception):
        WeatherInput(city="NYC", units="kelvin")


def test_agent_response_schema():
    r = AgentResponse(answer="42", tool_used="calculator_tool", steps=1)
    assert r.answer == "42"
    assert r.steps == 1


def test_agent_response_defaults():
    r = AgentResponse(answer="hello")
    assert r.tool_used is None
    assert r.steps == 0
