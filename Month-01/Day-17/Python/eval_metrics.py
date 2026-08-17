"""Information Retrieval & RAG Evaluation Metrics (Precision@K, Recall@K, MRR, NDCG)."""

import math
from typing import List, Set


def precision_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    """Calculate Precision@K: Fraction of top-k retrieved docs that are relevant."""
    if k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / k


def recall_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    """Calculate Recall@K: Fraction of relevant docs retrieved in top-k."""
    if not relevant_ids or k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / len(relevant_ids)


def reciprocal_rank(retrieved_ids: List[str], relevant_ids: Set[str]) -> float:
    """Calculate Reciprocal Rank (RR): 1 / rank of the first relevant document."""
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def dcg_at_k(retrieved_ids: List[str], relevance_scores: dict[str, float], k: int) -> float:
    """Calculate Discounted Cumulative Gain at K."""
    score = 0.0
    for i, doc_id in enumerate(retrieved_ids[:k], start=1):
        rel = relevance_scores.get(doc_id, 0.0)
        score += rel / math.log2(i + 1)
    return score


def ndcg_at_k(retrieved_ids: List[str], relevance_scores: dict[str, float], k: int) -> float:
    """Calculate Normalized Discounted Cumulative Gain at K."""
    dcg = dcg_at_k(retrieved_ids, relevance_scores, k)
    ideal_order = sorted(relevance_scores.keys(), key=lambda x: relevance_scores[x], reverse=True)
    idcg = dcg_at_k(ideal_order, relevance_scores, k)
    if idcg == 0:
        return 0.0
    return dcg / idcg


if __name__ == "__main__":
    retrieved = ["doc_A", "doc_B", "doc_C", "doc_D", "doc_E"]
    relevant = {"doc_B", "doc_D"}
    rel_scores = {"doc_B": 2.0, "doc_D": 3.0, "doc_A": 0.0, "doc_C": 1.0}

    print("Retrieved:", retrieved)
    print("Relevant:", relevant)
    print(f"Precision@3: {precision_at_k(retrieved, relevant, 3):.4f}")
    print(f"Recall@3:    {recall_at_k(retrieved, relevant, 3):.4f}")
    print(f"MRR:         {reciprocal_rank(retrieved, relevant):.4f}")
    print(f"NDCG@3:      {ndcg_at_k(retrieved, rel_scores, 3):.4f}")
