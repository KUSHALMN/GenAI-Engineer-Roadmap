"""
core/query_transformer.py — Query Rewriter & Web Fallback Simulator
Reformulates complex, ambiguous queries and routes to external web search.
"""
from typing import List


class QueryTransformer:
    def __init__(self):
        self.synonyms = {
            "lora": "low-rank adaptation",
            "qlora": "quantized low-rank adaptation",
            "mcp": "model context protocol",
            "crag": "corrective retrieval augmented generation",
        }

    def rewrite(self, query: str) -> str:
        rewritten = query.lower()
        for k, v in self.synonyms.items():
            if k in rewritten:
                rewritten = rewritten.replace(k, f"{k} ({v})")
        return rewritten

    def web_search(self, query: str) -> List[str]:
        """External search API fallback."""
        return [f"[Web Result] Verified external search documents addressing: '{query}'."]
