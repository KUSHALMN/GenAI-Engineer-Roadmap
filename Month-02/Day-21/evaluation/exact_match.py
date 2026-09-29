"""
exact_match.py — Exact match and normalized exact match evaluation.
"""
import re


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


def exact_match(prediction: str, expected: str) -> int:
    return int(prediction.strip() == expected.strip())


def normalized_exact_match(prediction: str, expected: str) -> int:
    return int(normalize(prediction) == normalize(expected))


def batch_exact_match(predictions: list, expected: list) -> dict:
    em = [exact_match(p, e) for p, e in zip(predictions, expected)]
    nem = [normalized_exact_match(p, e) for p, e in zip(predictions, expected)]
    return {
        "exact_match": round(sum(em) / len(em), 4),
        "normalized_exact_match": round(sum(nem) / len(nem), 4),
        "total": len(em),
    }
