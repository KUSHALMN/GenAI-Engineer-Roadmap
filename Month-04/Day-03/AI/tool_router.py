"""
Day 03: Tool Selection and Routing
Demonstrates intent matching, routing decisions across candidate tools,
disambiguation between competing tools, and fallback handling for unsupported requests.
"""

from typing import Dict, Any, List, Optional
import re

class ToolRouter:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Any]] = {}

    def add_tool_route(self, tool_name: str, keywords: List[str], description: str):
        self.routes[tool_name] = {
            "keywords": [kw.lower() for kw in keywords],
            "description": description
        }

    def route_query(self, user_query: str) -> Dict[str, Any]:
        """Classifies user intent and routes to best tool or requests clarification."""
        query_lower = user_query.lower()
        scores: Dict[str, int] = {}

        for tool_name, data in self.routes.items():
            score = 0
            for kw in data["keywords"]:
                if re.search(r"\b" + re.escape(kw) + r"\b", query_lower):
                    score += 2
                elif kw in query_lower:
                    score += 1
            if score > 0:
                scores[tool_name] = score

        if not scores:
            return {
                "action": "FALLBACK",
                "tool": None,
                "reason": "No registered tool matches the request intent."
            }

        sorted_tools = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_tool, best_score = sorted_tools[0]

        # Check for ambiguity (tie in score among top 2 tools)
        if len(sorted_tools) > 1 and sorted_tools[1][1] == best_score:
            return {
                "action": "DISAMBIGUATE",
                "candidates": [t[0] for t in sorted_tools if t[1] == best_score],
                "reason": "Multiple candidate tools match query with equal confidence."
            }

        return {
            "action": "ROUTE",
            "tool": best_tool,
            "confidence_score": best_score,
            "reason": f"Matched route for {best_tool}"
        }

if __name__ == "__main__":
    router = ToolRouter()
    router.add_tool_route("weather_tool", ["weather", "temperature", "forecast", "rain"], "Check weather conditions")
    router.add_tool_route("calculator_tool", ["calculate", "math", "add", "multiply", "sum"], "Evaluate math expressions")
    router.add_tool_route("database_query", ["sql", "database", "table", "rows", "records"], "Query internal relational DB")

    # Tests
    r1 = router.route_query("What is the temperature in San Francisco?")
    assert r1["action"] == "ROUTE" and r1["tool"] == "weather_tool"
    print(f"Direct Route Test: {r1}")

    r2 = router.route_query("Please calculate the sum of 10 and 25")
    assert r2["action"] == "ROUTE" and r2["tool"] == "calculator_tool"
    print(f"Calculator Route Test: {r2}")

    r3 = router.route_query("Tell me a funny joke about cats.")
    assert r3["action"] == "FALLBACK"
    print(f"Fallback Route Test: {r3}")

    print("Day 03 AI Tool Router passed all tests.")
