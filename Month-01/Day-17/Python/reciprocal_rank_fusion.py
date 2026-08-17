"""Reciprocal Rank Fusion (RRF) Implementation."""

from typing import Any, Dict, List


def reciprocal_rank_fusion(
    ranked_lists: List[List[Dict[str, Any]]],
    k: int = 60,
    top_n: int = 5,
    key_field: str = "id",
) -> List[Dict[str, Any]]:
    """Combines multiple ranked result lists using Reciprocal Rank Fusion.

    Formula: RRF_score(d) = sum_{m in models} 1 / (k + rank_m(d))
    """
    rrf_scores: Dict[Any, float] = {}
    doc_lookup: Dict[Any, Dict[str, Any]] = {}

    for ranked_list in ranked_lists:
        for rank, doc in enumerate(ranked_list, start=1):
            doc_id = doc[key_field]
            doc_lookup[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    sorted_ids = sorted(rrf_scores.keys(), key=lambda d_id: rrf_scores[d_id], reverse=True)

    final_results: List[Dict[str, Any]] = []
    for doc_id in sorted_ids[:top_n]:
        res = dict(doc_lookup[doc_id])
        res["rrf_score"] = round(rrf_scores[doc_id], 6)
        final_results.append(res)

    return final_results


if __name__ == "__main__":
    # Simulated semantic vector search results
    semantic_results = [
        {"id": "doc_1", "text": "Semantic search finds conceptual matches via embeddings."},
        {"id": "doc_2", "text": "Dense retrievers map sentences into vector spaces."},
        {"id": "doc_3", "text": "Hybrid search bridges keyword and semantic results."},
    ]

    # Simulated BM25 keyword search results
    keyword_results = [
        {"id": "doc_3", "text": "Hybrid search bridges keyword and semantic results."},
        {"id": "doc_4", "text": "BM25 scores exact terms matching queries."},
        {"id": "doc_1", "text": "Semantic search finds conceptual matches via embeddings."},
    ]

    fused = reciprocal_rank_fusion([semantic_results, keyword_results], k=60, top_n=3)

    print("=== Reciprocal Rank Fusion Results ===")
    for rank, doc in enumerate(fused, 1):
        print(f"Rank {rank}: [ID: {doc['id']}, RRF Score: {doc['rrf_score']}] - {doc['text']}")
