import re
from typing import List, Dict, Any
from collections import Counter

class CrossEncoderReranker:
    @staticmethod
    def _score_pair(query: str, document: str) -> float:
        q_tokens = re.findall(r"\b\w+\b", query.lower())
        d_tokens = re.findall(r"\b\w+\b", document.lower())
        if not q_tokens or not d_tokens:
            return 0.0
        d_counts = Counter(d_tokens)
        q_counts = Counter(q_tokens)
        overlap = sum(min(d_counts[w], 3) for w in q_counts.keys()) / (len(q_tokens) + 1e-5)
        phrase_bonus = 1.5 if " ".join(q_tokens) in " ".join(d_tokens) else 0.0
        return round(overlap + phrase_bonus, 4)

    @classmethod
    def rerank(cls, query: str, candidates: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        scored = []
        for doc in candidates:
            score = cls._score_pair(query, doc["content"])
            doc_copy = dict(doc)
            doc_copy["rerank_score"] = score
            scored.append(doc_copy)
        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_k]
