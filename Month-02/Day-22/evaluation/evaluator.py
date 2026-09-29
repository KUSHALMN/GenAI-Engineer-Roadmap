"""
evaluator.py — Advanced RAG evaluation orchestrator (Day 22).
Runs Token F1, Context Relevance, Faithfulness, and Answer Relevance.
"""
import json
from pathlib import Path
from exact_match import batch_exact_match
from keyword_match import batch_token_f1, context_relevance, faithfulness_score


def load_dataset(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def run_evaluation(dataset_path: str = "../data/eval_dataset.json") -> dict:
    samples = load_dataset(dataset_path)
    predictions = [s["prediction"] for s in samples]
    expected = [s["expected"] for s in samples]

    em_results = batch_exact_match(predictions, expected)
    f1_results = batch_token_f1(predictions, expected)

    ctx_scores = [context_relevance(s["question"], s["context"]) for s in samples]
    faith_scores = [faithfulness_score(s["prediction"], s["context"]) for s in samples]

    report = {
        "total_samples": len(samples),
        "exact_match": em_results,
        "token_f1": f1_results,
        "rag_triad": {
            "avg_context_relevance": round(sum(ctx_scores) / len(ctx_scores), 4),
            "avg_faithfulness": round(sum(faith_scores) / len(faith_scores), 4),
            "context_relevance_scores": ctx_scores,
            "faithfulness_scores": faith_scores,
        },
        "summary": {
            "exact_match": em_results["exact_match"],
            "avg_token_f1": f1_results["avg_token_f1"],
            "avg_context_relevance": round(sum(ctx_scores) / len(ctx_scores), 4),
            "avg_faithfulness": round(sum(faith_scores) / len(faith_scores), 4),
        }
    }

    out_path = Path("../results/evaluation_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"RAG Evaluation complete — {len(samples)} samples")
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")
    return report


if __name__ == "__main__":
    run_evaluation()
