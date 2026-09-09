"""
evaluate.py — Evaluate fine-tuned model responses against expected outputs.
Metrics: Exact Match, BLEU-1, and simple keyword overlap (F1).
"""
import json
import re
from pathlib import Path


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def bleu1(reference: str, hypothesis: str) -> float:
    ref_tokens = set(tokenize(reference))
    hyp_tokens = tokenize(hypothesis)
    if not hyp_tokens:
        return 0.0
    matches = sum(1 for t in hyp_tokens if t in ref_tokens)
    return round(matches / len(hyp_tokens), 4)


def keyword_f1(reference: str, hypothesis: str) -> float:
    ref = set(tokenize(reference))
    hyp = set(tokenize(hypothesis))
    if not hyp or not ref:
        return 0.0
    precision = len(ref & hyp) / len(hyp)
    recall = len(ref & hyp) / len(ref)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def evaluate(test_path: str = "evaluation/test_samples.jsonl"):
    if not Path(test_path).exists():
        print(f"No test file at {test_path}. Run prepare_dataset.py first.")
        return

    samples = [json.loads(l) for l in open(test_path) if l.strip()]
    results = []

    for s in samples:
        expected = s.get("expected", "")
        # In production: replace with actual model inference call
        predicted = expected  # stub: perfect prediction for demo

        results.append({
            "bleu1": bleu1(expected, predicted),
            "f1": keyword_f1(expected, predicted),
            "exact_match": int(expected.strip() == predicted.strip()),
        })

    avg_bleu = round(sum(r["bleu1"] for r in results) / len(results), 4)
    avg_f1 = round(sum(r["f1"] for r in results) / len(results), 4)
    avg_em = round(sum(r["exact_match"] for r in results) / len(results), 4)

    print(f"Evaluated {len(results)} samples")
    print(f"  BLEU-1:      {avg_bleu}")
    print(f"  Keyword F1:  {avg_f1}")
    print(f"  Exact Match: {avg_em}")
    return {"bleu1": avg_bleu, "f1": avg_f1, "exact_match": avg_em}


if __name__ == "__main__":
    evaluate()
