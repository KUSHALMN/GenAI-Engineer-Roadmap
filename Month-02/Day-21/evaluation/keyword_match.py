"""
keyword_match.py — Token-level F1 and keyword overlap scoring.
"""
import re


def tokenize(text: str) -> list:
    return re.findall(r"\w+", text.lower())


def token_f1(prediction: str, expected: str) -> float:
    pred_tokens = set(tokenize(prediction))
    exp_tokens = set(tokenize(expected))
    if not pred_tokens or not exp_tokens:
        return 0.0
    precision = len(pred_tokens & exp_tokens) / len(pred_tokens)
    recall = len(pred_tokens & exp_tokens) / len(exp_tokens)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def keyword_overlap(prediction: str, keywords: list) -> float:
    pred_tokens = set(tokenize(prediction))
    matched = sum(1 for kw in keywords if kw.lower() in pred_tokens)
    return round(matched / len(keywords), 4) if keywords else 0.0


def batch_token_f1(predictions: list, expected: list) -> dict:
    scores = [token_f1(p, e) for p, e in zip(predictions, expected)]
    return {
        "avg_token_f1": round(sum(scores) / len(scores), 4),
        "scores": scores,
        "total": len(scores),
    }
