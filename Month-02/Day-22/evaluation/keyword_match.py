"""
keyword_match.py — Token F1 + context relevance scoring for RAG (Day 22).
"""
import re


def tokenize(text: str) -> set:
    return set(re.findall(r"\w+", text.lower()))


def token_f1(prediction: str, expected: str) -> float:
    pred, exp = tokenize(prediction), tokenize(expected)
    if not pred or not exp:
        return 0.0
    precision = len(pred & exp) / len(pred)
    recall = len(pred & exp) / len(exp)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def context_relevance(question: str, context: str) -> float:
    """Measures how much of the question vocabulary appears in the context."""
    q_tokens = tokenize(question)
    c_tokens = tokenize(context)
    if not q_tokens:
        return 0.0
    return round(len(q_tokens & c_tokens) / len(q_tokens), 4)


def faithfulness_score(prediction: str, context: str) -> float:
    """Measures how much of the prediction is grounded in the context."""
    pred_tokens = tokenize(prediction)
    ctx_tokens = tokenize(context)
    if not pred_tokens:
        return 0.0
    return round(len(pred_tokens & ctx_tokens) / len(pred_tokens), 4)


def batch_token_f1(predictions: list, expected: list) -> dict:
    scores = [token_f1(p, e) for p, e in zip(predictions, expected)]
    return {
        "avg_token_f1": round(sum(scores) / len(scores), 4),
        "scores": scores,
        "total": len(scores),
    }
