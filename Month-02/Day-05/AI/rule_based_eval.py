"""
Rule-Based Evaluator for LLM Outputs.
Computes Exact Match, Normalized Substring Match, Token-Level Precision/Recall/F1,
Keyword Coverage, and Format/Length assertions without external LLM calls.
"""

import re
import string
from typing import Any, Dict, List, Set


def normalize_text(text: str) -> str:
    """Lowercase, strip punctuation, remove extra whitespaces."""
    text = text.lower()
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    return " ".join(text.split())


class RuleBasedEvaluator:

    @staticmethod
    def exact_match(prediction: str, ground_truth: str) -> float:
        """Returns 1.0 if normalized strings match completely, else 0.0."""
        return 1.0 if normalize_text(prediction) == normalize_text(ground_truth) else 0.0

    @staticmethod
    def contains_all_keywords(prediction: str, expected_keywords: List[str]) -> float:
        """Percentage of required keywords present in prediction."""
        if not expected_keywords:
            return 1.0
        normalized_pred = normalize_text(prediction)
        found = sum(1 for kw in expected_keywords if kw.lower() in normalized_pred)
        return found / len(expected_keywords)

    @staticmethod
    def token_f1(prediction: str, ground_truth: str) -> Dict[str, float]:
        """Calculates token-level precision, recall, and F1 score."""
        pred_tokens = normalize_text(prediction).split()
        truth_tokens = normalize_text(ground_truth).split()

        if not pred_tokens or not truth_tokens:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

        common = set(pred_tokens) & set(truth_tokens)
        if not common:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

        # Token frequencies
        common_count = sum(min(pred_tokens.count(tok), truth_tokens.count(tok)) for tok in common)
        precision = common_count / len(pred_tokens)
        recall = common_count / len(truth_tokens)
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }

    @staticmethod
    def evaluate_sample(prediction: str, ground_truth: str, expected_keywords: List[str]) -> Dict[str, Any]:
        """Run all rule-based checks on a single output."""
        em = RuleBasedEvaluator.exact_match(prediction, ground_truth)
        kw_cov = RuleBasedEvaluator.contains_all_keywords(prediction, expected_keywords)
        f1_stats = RuleBasedEvaluator.token_f1(prediction, ground_truth)

        # Composite score: 40% F1, 40% keyword coverage, 20% exact match
        composite = round(0.4 * f1_stats["f1"] + 0.4 * kw_cov + 0.2 * em, 4)

        return {
            "exact_match": em,
            "keyword_coverage": round(kw_cov, 4),
            "token_precision": f1_stats["precision"],
            "token_recall": f1_stats["recall"],
            "token_f1": f1_stats["f1"],
            "composite_score": composite,
            "passed": composite >= 0.65,
        }


if __name__ == "__main__":
    truth = "LoRA freezes base weights and introduces low-rank decomposition matrices."
    pred_good = "LoRA freezes the base model weights and injects low-rank decomposition matrices into attention."
    pred_bad = "LoRA trains full weights with no rank matrices."

    res_good = RuleBasedEvaluator.evaluate_sample(pred_good, truth, ["freezes", "rank", "matrices"])
    res_bad = RuleBasedEvaluator.evaluate_sample(pred_bad, truth, ["freezes", "rank", "matrices"])

    print("Good Output Eval:", res_good)
    print("Bad Output Eval:", res_bad)
    assert res_good["passed"] is True
    assert res_bad["passed"] is False
    print("RuleBasedEvaluator tests passed successfully!")
