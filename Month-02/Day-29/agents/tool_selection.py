"""Dynamic Tool Selection using semantic cosine matching and rule filters."""
import math
from typing import List, Dict, Any, Tuple


class ToolSelector:
    """Selects top-k tools relevant to current sub-goal to minimize context size."""

    def __init__(self):
        self.catalog = [
            {"name": "web_search", "desc": "Search public internet for recent facts, news, and live updates."},
            {"name": "sql_query", "desc": "Query enterprise PostgreSQL analytical warehouse for tables and records."},
            {"name": "calculator", "desc": "Perform exact mathematical formulas, mortgage amortization, and statistical arithmetic."},
            {"name": "file_reader", "desc": "Read local logs, markdown documentation, or PDF texts."},
        ]

    def _similarity(self, text_a: str, text_b: str) -> float:
        set_a = set(text_a.lower().split())
        set_b = set(text_b.lower().split())
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        return intersection / math.sqrt(len(set_a) * len(set_b))

    def select_tools(self, current_goal: str, top_k: int = 2) -> List[Dict[str, Any]]:
        scored = []
        for tool in self.catalog:
            score = self._similarity(current_goal, tool["desc"] + " " + tool["name"])
            scored.append((score, tool))

        scored.sort(key=lambda x: x[0], reverse=True)
        # Always return at least top_k tools
        return [t for _, t in scored[:top_k]]
