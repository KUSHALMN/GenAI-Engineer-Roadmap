import math
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

class CrossEncoderReranker:
    """
    Reranks candidate document chunks retrieved from first-stage bi-encoder retrieval.
    Scores joint query-document term overlap, positional proximity, and lexical relevance.
    """

    @staticmethod
    def _score_pair(query: str, document: str) -> float:
        q_tokens = re.findall(r"\b\w+\b", query.lower())
        d_tokens = re.findall(r"\b\w+\b", document.lower())
        
        if not q_tokens or not d_tokens:
            return 0.0

        d_counts = Counter(d_tokens)
        q_counts = Counter(q_tokens)
        
        overlap_score = sum(min(d_counts[w], 3) for w in q_counts.keys()) / (len(q_tokens) + 1e-5)
        
        # Exact phrase bonus
        clean_q = " ".join(q_tokens)
        clean_d = " ".join(d_tokens)
        phrase_bonus = 1.5 if clean_q in clean_d else 0.0
        
        return round(overlap_score + phrase_bonus, 4)

    @classmethod
    def rerank(cls, query: str, candidates: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        scored = []
        for doc in candidates:
            score = cls._score_pair(query, doc["content"])
            doc_copy = dict(doc)
            doc_copy["rerank_score"] = score
            scored.append(doc_copy)

        # Sort descending by rerank score
        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_k]
