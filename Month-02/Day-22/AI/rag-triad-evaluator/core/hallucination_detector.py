"""
core/hallucination_detector.py — Fine-Grained Sentence Grounding & Hallucination Detector
Flags unsupported claims, ungrounded numbers, and entity drift.
"""
import re
from typing import List, Dict, Any


def tokenize_words(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def extract_entities(text: str) -> List[str]:
    patterns = [
        r"\b[A-Z]{2,}\b",
        r"\b\d+(?:\.\d+)?%?\b",
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
    ]
    entities = set()
    for pat in patterns:
        for match in re.finditer(pat, text):
            entities.add(match.group(0))
    return list(entities)


def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


class HallucinationDetector:
    def __init__(self, token_overlap_threshold: float = 0.45):
        self.threshold = token_overlap_threshold

    def evaluate_sentence(self, sentence: str, context: str) -> Dict[str, Any]:
        s_words = set(tokenize_words(sentence))
        c_words = set(tokenize_words(context))

        if not s_words:
            return {"sentence": sentence, "grounded": True, "token_overlap": 1.0, "unsupported_entities": []}

        overlap = len(s_words & c_words) / len(s_words)
        sent_entities = extract_entities(sentence)
        unsupported = [e for e in sent_entities if e.lower() not in context.lower()]
        is_grounded = (overlap >= self.threshold) and (len(unsupported) == 0)

        return {
            "sentence": sentence,
            "grounded": is_grounded,
            "token_overlap": round(overlap, 4),
            "unsupported_entities": unsupported,
        }

    def evaluate(self, response: str, context: str) -> Dict[str, Any]:
        sentences = split_sentences(response)
        if not sentences:
            return {"hallucination_score": 0.0, "is_safe": True, "breakdown": []}

        breakdown = [self.evaluate_sentence(s, context) for s in sentences]
        ungrounded_count = sum(1 for b in breakdown if not b["grounded"])
        hallucination_score = round(ungrounded_count / len(sentences), 4)

        return {
            "total_sentences": len(sentences),
            "ungrounded_sentences": ungrounded_count,
            "hallucination_score": hallucination_score,
            "is_safe": hallucination_score <= 0.25,
            "breakdown": breakdown,
        }
