"""
model.py — LangChain Agent with custom tools (Search, Calculator, Weather).
Uses Groq as the LLM backend via ChatGroq.
"""
import os
import ast
import operator
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from schemas import SearchInput, CalculatorInput, WeatherInput

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.n
    if isinstance(node, ast.BinOp):
        return SAFE_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return SAFE_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression: {node}")


@tool(args_schema=SearchInput)
def search_tool(query: str, max_results: int = 3) -> str:
    """Search the web for information about a query."""
    # Stub: replace with real search API (SerpAPI, Tavily, etc.)
    return f"[Search results for '{query}']: Found {max_results} relevant articles about {query}."


@tool(args_schema=CalculatorInput)
def calculator_tool(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool(args_schema=WeatherInput)
def weather_tool(city: str, units: str = "celsius") -> str:
    """Get current weather for a city."""
    # Stub: replace with real weather API (OpenWeatherMap, etc.)
    unit_symbol = "°C" if units == "celsius" else "°F"
    temp = 22 if units == "celsius" else 72
    return f"Weather in {city}: {temp}{unit_symbol}, partly cloudy, humidity 65%."


TOOLS = [search_tool, calculator_tool, weather_tool]

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant with access to search, calculator, and weather tools. Use them when needed."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


def build_agent_executor() -> AgentExecutor:
    llm = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY, temperature=0)
    agent = create_tool_calling_agent(llm, TOOLS, PROMPT)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=5)
