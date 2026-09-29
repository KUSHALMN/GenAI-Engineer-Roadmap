"""
core/metrics.py — Lexical and Token-Level Evaluation Metrics
Provides Exact Match (EM), Normalized EM, Token Precision, Recall, and F1.
"""
import re
from typing import Dict, Any


def normalize_answer(text: str) -> str:
    """Lowercases text, removes punctuation, articles, and extra whitespace."""
    text = text.lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())


def exact_match(prediction: str, ground_truth: str) -> float:
    """Exact string identity check (1.0 or 0.0)."""
    return 1.0 if prediction.strip() == ground_truth.strip() else 0.0


def normalized_exact_match(prediction: str, ground_truth: str) -> float:
    """Exact match after text normalization (1.0 or 0.0)."""
    return 1.0 if normalize_answer(prediction) == normalize_answer(ground_truth) else 0.0


def token_f1(prediction: str, ground_truth: str) -> Dict[str, float]:
    """Calculates Token-level Precision, Recall, and F1 score."""
    p_tokens = normalize_answer(prediction).split()
    g_tokens = normalize_answer(ground_truth).split()

    if not p_tokens or not g_tokens:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    common = {}
    for token in p_tokens:
        if token in g_tokens:
            common[token] = min(p_tokens.count(token), g_tokens.count(token))

    overlap = sum(common.values())
    if overlap == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    precision = overlap / len(p_tokens)
    recall = overlap / len(g_tokens)
    f1 = 2 * (precision * recall) / (precision + recall)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def compute_lexical_metrics(prediction: str, ground_truth: str) -> Dict[str, Any]:
    """Runs all lexical metrics for a prediction and ground truth pair."""
    em = exact_match(prediction, ground_truth)
    norm_em = normalized_exact_match(prediction, ground_truth)
    f1_stats = token_f1(prediction, ground_truth)

    return {
        "exact_match": em,
        "normalized_exact_match": norm_em,
        **f1_stats,
    }
