from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag_pipeline import RAGPipeline


def load_dataset(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_metrics(
    pipeline: RAGPipeline, item: Dict[str, Any], retriever_type: str = "hybrid"
) -> Dict[str, Any]:
    question = item["question"]
    ground_truth = item["ground_truth_context"]
    expected_keywords = set(k.lower() for k in item.get("expected_keywords", []))

    start_t = time.perf_counter()
    retrieved = pipeline.retrieve_context(
        query=question, retriever_type=retriever_type, top_k=4, use_reranker=True
    )
    latency_ms = round((time.perf_counter() - start_t) * 1000, 2)

    retrieved_texts = [doc.get("text", "") for doc in retrieved]
    combined_text = " ".join(retrieved_texts).lower()

    # 1. Recall check: Is ground truth snippet found in top retrieved?
    ground_truth_words = set(ground_truth.lower().split())
    overlap_words = [w for w in ground_truth_words if w in combined_text]
    recall_score = len(overlap_words) / len(ground_truth_words) if ground_truth_words else 0.0

    # 2. Precision check: Rank position of best matching document
    best_rank = 0
    for rank, text in enumerate(retrieved_texts, start=1):
        if any(kw in text.lower() for kw in expected_keywords):
            best_rank = rank
            break
    precision_reciprocal_rank = 1.0 / best_rank if best_rank > 0 else 0.0

    # 3. Keyword hit ratio
    keyword_hits = sum(1 for kw in expected_keywords if kw in combined_text)
    keyword_hit_ratio = keyword_hits / len(expected_keywords) if expected_keywords else 1.0

    return {
        "question_id": item["id"],
        "question": question,
        "retrieved_count": len(retrieved),
        "hit_at_rank": best_rank,
        "mrr": round(precision_reciprocal_rank, 4),
        "keyword_coverage": round(keyword_hit_ratio, 4),
        "recall_score": round(recall_score, 4),
        "latency_ms": latency_ms,
    }


def run_evaluation() -> Dict[str, Any]:
    eval_dir = Path(__file__).parent
    questions_file = eval_dir / "questions.json"
    results_file = eval_dir / "results.json"

    items = load_dataset(questions_file)

    # Instantiate pipeline and populate index with all ground truth texts
    pipeline = RAGPipeline()
    pipeline.clear()

    for idx, item in enumerate(items):
        pipeline.ingest_raw_text(
            item["ground_truth_context"], source_name=f"eval_gt_doc_{idx+1}"
        )

    evaluations = []
    for item in items:
        metric = calculate_metrics(pipeline, item, retriever_type="hybrid")
        evaluations.append(metric)

    avg_mrr = sum(e["mrr"] for e in evaluations) / len(evaluations)
    avg_recall = sum(e["recall_score"] for e in evaluations) / len(evaluations)
    avg_keyword_coverage = sum(e["keyword_coverage"] for e in evaluations) / len(evaluations)
    avg_latency_ms = sum(e["latency_ms"] for e in evaluations) / len(evaluations)

    summary = {
        "benchmark_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_test_cases": len(evaluations),
        "metrics_summary": {
            "mean_reciprocal_rank_mrr": round(avg_mrr, 4),
            "mean_recall": round(avg_recall, 4),
            "mean_keyword_coverage": round(avg_keyword_coverage, 4),
            "average_latency_ms": round(avg_latency_ms, 2),
        },
        "detailed_results": evaluations,
    }

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=== Evaluation Summary ===")
    print(f"Total Test Cases: {summary['total_test_cases']}")
    print(f"MRR (Mean Reciprocal Rank): {summary['metrics_summary']['mean_reciprocal_rank_mrr']}")
    print(f"Mean Recall: {summary['metrics_summary']['mean_recall']}")
    print(f"Mean Keyword Coverage: {summary['metrics_summary']['mean_keyword_coverage']}")
    print(f"Avg Latency: {summary['metrics_summary']['average_latency_ms']} ms")
    print(f"Results saved to: {results_file}")

    return summary


if __name__ == "__main__":
    run_evaluation()
