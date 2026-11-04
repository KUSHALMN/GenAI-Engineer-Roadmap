"""
HyDE (Hypothetical Document Embeddings) Retrieval Engine
Generates a zero-shot hypothetical answer to bridge the embedding representation gap
between short questions and long document passages.
"""

import math
from typing import List, Dict, Any, Tuple


class HyDERetriever:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus
        self.doc_vectors = [self._embed(d["text"]) for d in corpus]

    def _embed(self, text: str) -> List[float]:
        """Simple deterministic term-frequency vector embedding for local benchmarking"""
        vec = [0.0] * 32
        for i, word in enumerate(text.lower().split()):
            h = hash(word) % 32
            vec[h] += 1.0 / (1 + (i % 5))
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def generate_hypothetical_document(self, query: str) -> str:
        """
        Simulates an LLM zero-shot response to a question.
        In production, this calls a fast instruction-following LLM with temperature=0.3.
        """
        q_lower = query.lower()
        if "pgvector" in q_lower or "postgres" in q_lower:
            return (
                "PostgreSQL pgvector extension enables relational databases to store vector embeddings "
                "alongside structured transactional rows. It provides HNSW and IVFFlat indices, allowing "
                "vector cosine distance queries directly using SQL operators."
            )
        elif "dsu" in q_lower or "union find" in q_lower:
            return (
                "Disjoint Set Union (DSU) tracks elements partitioned into disjoint subsets. "
                "With path compression and union by rank, operations run in nearly O(1) amortized time."
            )
        else:
            return f"This document comprehensively explains {query} with detailed architectural specifications and practical patterns."

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def search_raw(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Standard direct query-to-document vector search"""
        q_vec = self._embed(query)
        scored = []
        for idx, d_vec in enumerate(self.doc_vectors):
            sim = self._cosine_similarity(q_vec, d_vec)
            scored.append((sim, self.corpus[idx]))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": d["id"], "score": round(s, 4), "text": d["text"]} for s, d in scored[:top_k]]

    def search_hyde(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """HyDE search: embeds hypothetical answer instead of user question"""
        hypothetical_doc = self.generate_hypothetical_document(query)
        hypo_vec = self._embed(hypothetical_doc)

        scored = []
        for idx, d_vec in enumerate(self.doc_vectors):
            sim = self._cosine_similarity(hypo_vec, d_vec)
            scored.append((sim, self.corpus[idx]))
        scored.sort(key=lambda x: x[0], reverse=True)

        return {
            "query": query,
            "hypothetical_document": hypothetical_doc,
            "results": [{"id": d["id"], "score": round(s, 4), "text": d["text"]} for s, d in scored[:top_k]]
        }


if __name__ == "__main__":
    docs = [
        {"id": "d1", "text": "PostgreSQL relational databases support vector similarity search with pgvector extension HNSW."},
        {"id": "d2", "text": "Elasticsearch inverted index supports BM25 text ranking and faceted search queries."},
        {"id": "d3", "text": "Graph databases like Neo4j optimize recursive graph traversals and property graphs."},
        {"id": "d4", "text": "Disjoint set union data structures maintain connected components dynamically in O(alpha(N))."}
    ]

    retriever = HyDERetriever(docs)
    test_q = "How does pgvector work in Postgres?"

    raw_results = retriever.search_raw(test_q, top_k=2)
    hyde_results = retriever.search_hyde(test_q, top_k=2)

    print("=== Raw Query Vector Search ===")
    for r in raw_results:
        print(f"[{r['id']}] score={r['score']} -> {r['text']}")

    print("\n=== HyDE (Hypothetical Document Embeddings) ===")
    print(f"Hypothetical Doc: \"{hyde_results['hypothetical_document'][:80]}...\"")
    for r in hyde_results["results"]:
        print(f"[{r['id']}] score={r['score']} -> {r['text']}")
