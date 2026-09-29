"""
app/runner.py — RAG Triad & Hallucination Batch Runner
"""
import os
import json
from typing import Dict, Any
from core.triad_metrics import compute_rag_triad
from core.hallucination_detector import HallucinationDetector
from core.llm_judge import llm_rag_triad_judge


def run_pipeline(dataset_path: str = "data/eval_dataset.json", use_llm_judge: bool = True) -> Dict[str, Any]:
    if not os.path.exists(dataset_path):
        base = os.path.dirname(os.path.dirname(__file__))
        dataset_path = os.path.join(base, "data", "eval_dataset.json")

    with open(dataset_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    detector = HallucinationDetector()
    results = []

    for s in samples:
        q = s["question"]
        c = s["context"]
        ans = s.get("prediction", s.get("answer", ""))

        triad = compute_rag_triad(q, c, ans)
        hallucination = detector.evaluate(ans, c)

        item = {
            "id": s.get("id"),
            "question": q,
            "prediction": ans,
            "triad_metrics": triad,
            "hallucination_metrics": {
                "score": hallucination["hallucination_score"],
                "is_safe": hallucination["is_safe"],
                "ungrounded_sentences": hallucination["ungrounded_sentences"]
            }
        }

        if use_llm_judge:
            item["judge_scores"] = llm_rag_triad_judge(q, c, ans)

        results.append(item)

    avg = lambda k: round(sum(r["triad_metrics"][k] for r in results) / len(results), 4) if results else 0.0

    return {
        "samples_evaluated": len(results),
        "mean_context_relevance": avg("context_relevance"),
        "mean_faithfulness": avg("faithfulness"),
        "mean_answer_relevance": avg("answer_relevance"),
        "mean_composite": avg("composite_score"),
        "results": results
    }


if __name__ == "__main__":
    print("[RUN] Running Day 22 RAG Triad Pipeline...")
    res = run_pipeline(use_llm_judge=False)
    print(f"Evaluated Samples: {res['samples_evaluated']}")
    print(f"Mean Composite:    {res['mean_composite']}")
    print(f"Mean Faithfulness: {res['mean_faithfulness']}")
