"""
core/retrieval_evaluator.py — CRAG Retrieval Evaluator
Categorizes retrieved documents into:
- CORRECT: High confidence, triggers knowledge refinement
- AMBIGUOUS: Moderate confidence, combines local refinement with web search
- INCORRECT: Low confidence, discards docs and triggers web search / query reformulation
"""
import re
from typing import List, Dict, Tuple


class RetrievalEvaluator:
    def __init__(self, upper_threshold: float = 0.35, lower_threshold: float = 0.15):
        self.upper = upper_threshold
        self.lower = lower_threshold

    def evaluate(self, query: str, docs: List[Dict[str, str]]) -> Tuple[str, float]:
        if not docs:
            return "INCORRECT", 0.0

        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        scores = []
        for d in docs:
            full_text = (d.get("title", "") + " " + d.get("content", "")).lower()
            c_tokens = set(re.findall(r"\b\w+\b", full_text))
            score = len(q_tokens & c_tokens) / len(q_tokens) if q_tokens else 0.0
            scores.append(score)

        avg_score = sum(scores) / len(scores)

        if avg_score >= self.upper:
            return "CORRECT", round(avg_score, 4)
        elif avg_score >= self.lower:
            return "AMBIGUOUS", round(avg_score, 4)
        else:
            return "INCORRECT", round(avg_score, 4)
