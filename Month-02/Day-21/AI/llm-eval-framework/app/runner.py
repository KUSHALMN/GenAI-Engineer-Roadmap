"""
app/runner.py — Evaluation Pipeline Runner
Executes comprehensive evaluation combining Lexical Metrics & LLM-as-a-Judge.
"""
import os
import json
from typing import List, Dict, Any
from core.metrics import compute_lexical_metrics
from core.llm_judge import evaluate_with_llm_judge


def run_pipeline(dataset_path: str = "data/eval_dataset.json", use_llm_judge: bool = True) -> Dict[str, Any]:
    """Runs end-to-end evaluation pipeline on dataset."""
    if not os.path.exists(dataset_path):
        # Fallback to local data dir if run from different cwd
        base = os.path.dirname(os.path.dirname(__file__))
        dataset_path = os.path.join(base, "data", "eval_dataset.json")

    with open(dataset_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    results = []
    for s in samples:
        prediction = s.get("prediction", s.get("expected", ""))
        expected = s.get("expected", "")
        question = s.get("question", "")
        context = s.get("context", "")

        lexical = compute_lexical_metrics(prediction, expected)
        item = {
            "id": s.get("id"),
            "question": question,
            "prediction": prediction,
            "expected": expected,
            "metrics": lexical,
        }

        if use_llm_judge:
            item["judge"] = evaluate_with_llm_judge(question, context, expected, prediction)

        results.append(item)

    avg = lambda k: round(sum(r["metrics"][k] for r in results) / len(results), 4) if results else 0.0

    summary = {
        "total_samples": len(results),
        "mean_exact_match": avg("exact_match"),
        "mean_normalized_exact_match": avg("normalized_exact_match"),
        "mean_token_f1": avg("f1"),
        "mean_precision": avg("precision"),
        "mean_recall": avg("recall"),
        "results": results,
    }

    return summary


if __name__ == "__main__":
    print("[RUN] Executing Day 21 Evaluation Pipeline...")
    report = run_pipeline(use_llm_judge=False)
    print(f"Total Samples: {report['total_samples']}")
    print(f"Mean Token F1: {report['mean_token_f1']}")
    print(f"Mean Norm EM:  {report['mean_normalized_exact_match']}")
