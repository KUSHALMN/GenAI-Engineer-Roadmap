"""
Query Router & Dynamic Execution Dispatcher
Classifies incoming user intent and dispatches queries to optimal specialized paths:
1. DIRECT_LLM (No retrieval needed: greetings, chit-chat, simple arithmetic)
2. KEYWORD_BM25 (Exact terms, error codes, part numbers, acronyms)
3. DENSE_SEMANTIC (Conceptual questions, fuzzy explanations, analogies)
4. MULTI_HOP_GRAPH (Complex relational questions requiring cross-document joins)
5. STRUCTURED_SQL (Aggregations, counts, metrics, tabular database lookups)
"""

import re
from typing import Dict, Any


class QueryRouter:
    def __init__(self):
        # Heuristic rules & intent patterns
        self.sql_keywords = {"how many", "total count", "average", "maximum", "minimum", "sum of", "filter by price"}
        self.greeting_patterns = re.compile(r'^(hi|hello|hey|good morning|thanks|thank you|bye)\b', re.IGNORECASE)
        self.exact_code_patterns = re.compile(r'\b(error\s*\d+|0x[0-9a-fA-F]+|[A-Z]{2,}-\d{3,})\b')
        self.multi_hop_triggers = {"who is the ceo of the company that", "which subsidiary of", "connected to", "invested in and founded"}

    def route_query(self, query: str) -> Dict[str, Any]:
        q = query.strip()
        q_lower = q.lower()

        # Route 1: Direct LLM (Zero-retrieval)
        if self.greeting_patterns.match(q_lower) or len(q.split()) <= 2 and not self.exact_code_patterns.search(q):
            return {
                "query": query,
                "route": "DIRECT_LLM",
                "target_engine": "llm_direct_responder",
                "estimated_latency_ms": 150,
                "reasoning": "Conversational greeting or generic interaction requiring no external knowledge."
            }

        # Route 2: Structured SQL / Analytical Database
        if any(keyword in q_lower for keyword in self.sql_keywords):
            return {
                "query": query,
                "route": "STRUCTURED_SQL",
                "target_engine": "text_to_sql_executor",
                "estimated_latency_ms": 300,
                "reasoning": "Numerical aggregation or tabular calculation detected."
            }

        # Route 3: Multi-Hop Relational Graph
        if any(trigger in q_lower for trigger in self.multi_hop_triggers) or "both" in q_lower:
            return {
                "query": query,
                "route": "MULTI_HOP_GRAPH",
                "target_engine": "graph_rag_traversal",
                "estimated_latency_ms": 800,
                "reasoning": "Complex multi-entity relational join detected."
            }

        # Route 4: Exact Keyword / BM25
        if self.exact_code_patterns.search(q):
            return {
                "query": query,
                "route": "KEYWORD_BM25",
                "target_engine": "sparse_bm25_search",
                "estimated_latency_ms": 25,
                "reasoning": "Exact error code, hex address, or SKU pattern identified."
            }

        # Route 5: Default Dense Vector Semantic Search
        return {
            "query": query,
            "route": "DENSE_SEMANTIC",
            "target_engine": "vector_hnsw_retriever",
            "estimated_latency_ms": 45,
            "reasoning": "Standard semantic explanatory question."
        }


if __name__ == "__main__":
    router = QueryRouter()

    test_queries = [
        "Hello, how are you today?",
        "What is the average salary of engineers hired in 2024?",
        "Error 404 in module AUTH-9921 connection refused",
        "Who is the CEO of the company that acquired DeepMind?",
        "Explain the intuition behind self-attention in transformers."
    ]

    print("=== Query Routing Engine Benchmark ===")
    for q in test_queries:
        r = router.route_query(q)
        print(f"Query: \"{q}\"")
        print(f"  -> Route: {r['route']} | Engine: {r['target_engine']} (Est: {r['estimated_latency_ms']}ms)")
        print(f"  -> Reason: {r['reasoning']}\n")
