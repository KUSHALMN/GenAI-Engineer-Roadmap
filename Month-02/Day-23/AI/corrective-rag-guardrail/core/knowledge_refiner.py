"""
core/knowledge_refiner.py — Knowledge Striping & Noise Elimination
Decomposes coarse retrieved chunks into fine-grained sentence strips
and discards irrelevant noise.
"""
import re
from typing import List, Dict


class KnowledgeRefiner:
    @staticmethod
    def refine(docs: List[Dict[str, str]], query: str) -> List[str]:
        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        refined_strips = []

        for doc in docs:
            sentences = re.split(r"(?<=[.!?])\s+", doc.get("content", ""))
            for s in sentences:
                s_clean = s.strip()
                if not s_clean:
                    continue
                s_tokens = set(re.findall(r"\b\w+\b", s_clean.lower()))
                if len(q_tokens & s_tokens) > 0:
                    refined_strips.append(s_clean)

        return refined_strips
