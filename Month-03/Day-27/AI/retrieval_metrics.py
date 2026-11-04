"""
Information Retrieval (IR) Evaluation Metrics Engine
Computes:
1. Precision@K = |Retrieved@K ∩ Relevant| / K
2. Recall@K    = |Retrieved@K ∩ Relevant| / |Relevant|
3. MRR (Mean Reciprocal Rank) = (1 / |Q|) * sum(1 / rank_first_relevant)
4. MAP (Mean Average Precision)
5. NDCG@K (Normalized Discounted Cumulative Gain) with graded relevance
"""

import math
from typing import List, Dict, Any, Set


class RetrievalMetrics:

    @staticmethod
    def precision_at_k(retrieved: List[str], ground_truth: Set[str], k: int) -> float:
        if k <= 0:
            return 0.0
        top_k = retrieved[:k]
        hits = sum(1 for doc in top_k if doc in ground_truth)
        return hits / float(k)

    @staticmethod
    def recall_at_k(retrieved: List[str], ground_truth: Set[str], k: int) -> float:
        if not ground_truth:
            return 1.0  # Vacuously true if no ground truth needed
        top_k = retrieved[:k]
        hits = sum(1 for doc in top_k if doc in ground_truth)
        return hits / float(len(ground_truth))

    @staticmethod
    def reciprocal_rank(retrieved: List[str], ground_truth: Set[str]) -> float:
        for rank, doc in enumerate(retrieved, start=1):
            if doc in ground_truth:
                return 1.0 / rank
        return 0.0

    @staticmethod
    def average_precision(retrieved: List[str], ground_truth: Set[str], k: int = 10) -> float:
        if not ground_truth:
            return 1.0
        score = 0.0
        hits = 0
        top_k = retrieved[:k]
        for rank, doc in enumerate(top_k, start=1):
            if doc in ground_truth:
                hits += 1
                score += hits / rank
        return score / min(len(ground_truth), k) if ground_truth else 0.0

    @staticmethod
    def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
        """
        DCG@K = sum((2^rel - 1) / log2(rank + 1))
        IDCG@K = ideal DCG sorting true relevances descending
        """
        top_k = retrieved[:k]
        dcg = 0.0
        for rank, doc in enumerate(top_k, start=1):
            rel = relevance_scores.get(doc, 0.0)
            dcg += (math.pow(2, rel) - 1.0) / math.log2(rank + 1)

        # Compute Ideal DCG
        ideal_rels = sorted(relevance_scores.values(), reverse=True)[:k]
        idcg = 0.0
        for rank, rel in enumerate(ideal_rels, start=1):
            idcg += (math.pow(2, rel) - 1.0) / math.log2(rank + 1)

        return (dcg / idcg) if idcg > 0.0 else 0.0

    @classmethod
    def evaluate_run(
        cls,
        eval_cases: List[Dict[str, Any]],
        k_values: List[int] = [1, 3, 5]
    ) -> Dict[str, Any]:
        """
        eval_cases format:
        [
          {"retrieved": ["d1", "d2", "d3"], "ground_truth": {"d1", "d3"}, "relevances": {"d1": 2.0, "d3": 3.0}}
        ]
        """
        total = len(eval_cases)
        mrr_sum = 0.0
        map_sum = 0.0
        precisions = {k: 0.0 for k in k_values}
        recalls = {k: 0.0 for k in k_values}
        ndcgs = {k: 0.0 for k in k_values}

        for case in eval_cases:
            ret = case["retrieved"]
            gt = set(case["ground_truth"])
            rels = case.get("relevances", {doc: 1.0 for doc in gt})

            mrr_sum += cls.reciprocal_rank(ret, gt)
            map_sum += cls.average_precision(ret, gt, k=max(k_values))

            for k in k_values:
                precisions[k] += cls.precision_at_k(ret, gt, k)
                recalls[k] += cls.recall_at_k(ret, gt, k)
                ndcgs[k] += cls.ndcg_at_k(ret, rels, k)

        return {
            "total_queries_evaluated": total,
            "MRR": round(mrr_sum / total, 4),
            "MAP": round(map_sum / total, 4),
            "Precision": {f"P@{k}": round(v / total, 4) for k, v in precisions.items()},
            "Recall": {f"R@{k}": round(v / total, 4) for k, v in recalls.items()},
            "NDCG": {f"NDCG@{k}": round(v / total, 4) for k, v in ndcgs.items()}
        }


if __name__ == "__main__":
    benchmark_cases = [
        {
            "query_id": "q1",
            "retrieved": ["doc_A", "doc_B", "doc_C", "doc_D"],
            "ground_truth": ["doc_A", "doc_C"],
            "relevances": {"doc_A": 3.0, "doc_C": 2.0}
        },
        {
            "query_id": "q2",
            "retrieved": ["doc_X", "doc_Y", "doc_Z"],
            "ground_truth": ["doc_Y"],
            "relevances": {"doc_Y": 3.0}
        }
    ]

    report = RetrievalMetrics.evaluate_run(benchmark_cases, k_values=[1, 3, 5])

    print("=== Multi-Metric Retrieval Evaluation Report ===")
    print(f"Evaluated Queries: {report['total_queries_evaluated']}")
    print(f"Mean Reciprocal Rank (MRR): {report['MRR']}")
    print(f"Mean Average Precision (MAP): {report['MAP']}")
    print("\nPrecision Metrics:", report["Precision"])
    print("Recall Metrics:   ", report["Recall"])
    print("NDCG Metrics:     ", report["NDCG"])
