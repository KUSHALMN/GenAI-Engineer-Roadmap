"""
Query Rewriting & Query Expansion Module for Advanced RAG.
Techniques:
1. HyDE (Hypothetical Document Embeddings): Generates a hypothetical ideal answer to bridge vocabulary gap.
2. Sub-Query Decomposition: Breaks complex multi-hop queries into atomic sub-questions.
3. Keyword Expansion: Adds synonyms and technical terms.
"""

from typing import Callable, Dict, List, Optional


class QueryRewriter:

    def __init__(self, llm_caller: Optional[Callable[[str], str]] = None):
        self.llm_caller = llm_caller or self._mock_llm

    def _mock_llm(self, prompt: str) -> str:
        """Simulate LLM transformations."""
        if "Hypothetical Document" in prompt:
            return "Hypothetical answer: Modern transformer models rely on self-attention and feedforward layers to process sequences in parallel."
        elif "sub-queries" in prompt:
            return "1. What is the architecture of transformers?\n2. What is self-attention mechanism?"
        return prompt

    def generate_hyde_doc(self, query: str) -> str:
        """Generates a hypothetical document answering the query."""
        prompt = f"Write a clear, authoritative passage answering this query for search retrieval:\nQuery: {query}\nHypothetical Document:"
        return self.llm_caller(prompt).strip()

    def decompose_query(self, query: str) -> List[str]:
        """Decomposes complex multi-part query into atomic sub-queries."""
        prompt = f"Decompose this complex query into 2-3 focused sub-queries for document retrieval:\nQuery: {query}"
        raw_output = self.llm_caller(prompt)
        sub_queries = []
        for line in raw_output.split("\n"):
            cleaned = line.strip().lstrip("0123456789.- ")
            if cleaned:
                sub_queries.append(cleaned)
        return sub_queries if sub_queries else [query]

    @staticmethod
    def expand_keywords(query: str) -> str:
        """Appends domain-specific synonyms and variant terms."""
        synonyms = {
            "rag": "retrieval augmented generation vector search embeddings",
            "llm": "large language model generative ai",
            "cache": "caching ttl memoization lru",
        }
        words = query.lower().split()
        expanded = list(words)
        for w in words:
            if w in synonyms:
                expanded.extend(synonyms[w].split())
        return " ".join(dict.fromkeys(expanded))  # preserve order & unique


if __name__ == "__main__":
    rewriter = QueryRewriter()

    # 1. HyDE
    hyde = rewriter.generate_hyde_doc("How do transformers work?")
    assert "self-attention" in hyde
    print("HyDE Document:", hyde)

    # 2. Decompose
    subs = rewriter.decompose_query("Compare transformers and RNNs")
    assert len(subs) >= 2
    print("Sub-queries:", subs)

    # 3. Expand
    expanded = rewriter.expand_keywords("Optimize RAG cache")
    assert "embeddings" in expanded
    print("Expanded Keywords:", expanded)

    print("QueryRewriter tests passed successfully!")
