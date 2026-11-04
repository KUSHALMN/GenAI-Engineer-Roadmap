"""
Multi-Query Retrieval Engine
Generates multiple perspectives/sub-queries for a single user question, executes independent
retrievals, deduplicates chunks by content hash / document ID, and preserves provenance.
"""

import hashlib
from typing import List, Dict, Any, Set


class MultiQueryRetriever:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus

    def generate_subqueries(self, query: str) -> List[str]:
        """
        Synthesizes diverse query formulations covering:
        1. Original user query
        2. Technical/formal perspective
        3. Implementation/code-centric perspective
        4. Architecture/system-level perspective
        """
        base = query.strip()
        subqueries = [
            base,
            f"technical architecture and internals of {base}",
            f"how to implement {base} best practices",
            f"key trade-offs and performance characteristics of {base}"
        ]
        return subqueries

    def _score_doc(self, subquery: str, doc: Dict[str, Any]) -> float:
        """Simple token overlap relevance score"""
        q_tokens = set(subquery.lower().split())
        d_tokens = set(doc["text"].lower().split())
        overlap = len(q_tokens.intersection(d_tokens))
        return overlap / (len(q_tokens) + 1e-5)

    def retrieve_and_deduplicate(self, query: str, top_k_per_query: int = 3) -> Dict[str, Any]:
        subqueries = self.generate_subqueries(query)
        seen_hashes: Set[str] = set()
        merged_results: List[Dict[str, Any]] = []

        for sub_q in subqueries:
            scored = []
            for doc in self.corpus:
                score = self._score_doc(sub_q, doc)
                if score > 0:
                    scored.append((score, doc))
            scored.sort(key=lambda x: x[0], reverse=True)

            for score, doc in scored[:top_k_per_query]:
                # Content hash for deduplication
                content_hash = hashlib.sha256(doc["text"].encode("utf-8")).hexdigest()[:12]
                if content_hash not in seen_hashes:
                    seen_hashes.add(content_hash)
                    merged_results.append({
                        "id": doc["id"],
                        "text": doc["text"],
                        "score": round(score, 4),
                        "provenance_query": sub_q,
                        "content_hash": content_hash
                    })

        # Final re-ranking by score
        merged_results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "original_query": query,
            "generated_subqueries": subqueries,
            "total_retrieved": len(merged_results),
            "results": merged_results
        }


if __name__ == "__main__":
    docs = [
        {"id": "c1", "text": "RAG systems use vector databases like Weaviate and Milvus for approximate nearest neighbor retrieval."},
        {"id": "c2", "text": "How to implement RAG best practices including hybrid search and cross-encoder reranking."},
        {"id": "c3", "text": "Key trade-offs and performance characteristics of RAG include latency overhead and index memory size."},
        {"id": "c4", "text": "Kubernetes container orchestration patterns for microservices deployments."},
        {"id": "c5", "text": "Technical architecture and internals of RAG vector index graphs such as HNSW."}
    ]

    retriever = MultiQueryRetriever(docs)
    out = retriever.retrieve_and_deduplicate("RAG architecture")

    print(f"Generated {len(out['generated_subqueries'])} Sub-queries:")
    for sq in out["generated_subqueries"]:
        print(f" - {sq}")

    print(f"\nRetrieved {out['total_retrieved']} Unique Chunks:")
    for res in out["results"]:
        print(f"[{res['id']}] (score: {res['score']}) -> {res['text'][:65]}... (via '{res['provenance_query'][:30]}...')")
