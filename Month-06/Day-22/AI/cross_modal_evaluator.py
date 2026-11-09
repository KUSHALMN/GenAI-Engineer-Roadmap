"""
Cross-Modal Retrieval Evaluation Suite.
Measures Recall@K, Mean Reciprocal Rank (MRR), and Normalized Discounted
Cumulative Gain (NDCG@K) across text-image and text-audio search queries.
"""

from dataclasses import dataclass
import math
from typing import Dict, List, Tuple


class CrossModalEvaluator:
    @staticmethod
    def evaluate_retrieval(queries_ground_truth: Dict[str, str], retrieved_rankings: Dict[str, List[str]], k: int = 3) -> Dict[str, float]:
        hits_at_k = 0
        reciprocal_ranks = []
        ndcg_scores = []

        for q, gold_doc in queries_ground_truth.items():
            ranking = retrieved_rankings.get(q, [])[:k]
            if gold_doc in ranking:
                hits_at_k += 1
                rank = ranking.index(gold_doc) + 1
                reciprocal_ranks.append(1.0 / rank)
                ndcg_scores.append(1.0 / math.log2(rank + 1))
            else:
                reciprocal_ranks.append(0.0)
                ndcg_scores.append(0.0)

        total = max(1, len(queries_ground_truth))
        return {
            f"Recall@{k}": round(hits_at_k / total, 4),
            "MRR": round(sum(reciprocal_ranks) / total, 4),
            f"NDCG@{k}": round(sum(ndcg_scores) / total, 4)
        }


if __name__ == "__main__":
    evaluator = CrossModalEvaluator()
    ground_truth = {"q1": "doc_A", "q2": "doc_B", "q3": "doc_C"}
    retrieved = {
        "q1": ["doc_A", "doc_X", "doc_Y"],
        "q2": ["doc_Z", "doc_B", "doc_M"],
        "q3": ["doc_W", "doc_K", "doc_C"]
    }
    metrics = evaluator.evaluate_retrieval(ground_truth, retrieved, k=3)
    print("=== Cross-Modal IR Metrics Benchmark ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
