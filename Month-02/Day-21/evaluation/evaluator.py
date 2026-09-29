"""
evaluator.py — Main evaluation orchestrator combining all metrics.
"""
import json
from pathlib import Path
from exact_match import batch_exact_match
from keyword_match import batch_token_f1


def load_dataset(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def run_evaluation(dataset_path: str = "../data/eval_dataset.json") -> dict:
    samples = load_dataset(dataset_path)

    # Stub predictions — replace with actual model inference
    predictions = [s["expected"] for s in samples]
    expected = [s["expected"] for s in samples]

    em_results = batch_exact_match(predictions, expected)
    f1_results = batch_token_f1(predictions, expected)

    report = {
        "total_samples": len(samples),
        "exact_match": em_results,
        "token_f1": f1_results,
        "summary": {
            "exact_match": em_results["exact_match"],
            "normalized_exact_match": em_results["normalized_exact_match"],
            "avg_token_f1": f1_results["avg_token_f1"],
        }
    }

    out_path = Path("../results/evaluation_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Evaluation complete — {len(samples)} samples")
    print(f"  Exact Match:      {report['summary']['exact_match']}")
    print(f"  Norm Exact Match: {report['summary']['normalized_exact_match']}")
    print(f"  Avg Token F1:     {report['summary']['avg_token_f1']}")
    return report


if __name__ == "__main__":
    run_evaluation()
