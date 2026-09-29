"""
core/self_rag_guardrail.py — Self-RAG Reflection Tokens & Auto-Repair Guardrails
Evaluates [Retrieve], [IsRel], [IsSup], [IsUse] tokens with automatic self-correction.
"""
import re
from typing import Dict, Any


class SelfRAGGuardrail:
    def __init__(self, support_threshold: float = 0.5):
        self.support_threshold = support_threshold

    def evaluate_retrieval_need(self, query: str) -> str:
        keywords = ["what", "how", "why", "difference", "explain", "architecture", "algorithm", "compare"]
        tokens = set(re.findall(r"\b\w+\b", query.lower()))
        return "Yes" if any(k in tokens for k in keywords) else "No"

    def evaluate_relevance(self, context: str, query: str) -> str:
        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        c_tokens = set(re.findall(r"\b\w+\b", context.lower()))
        overlap = len(q_tokens & c_tokens) / len(q_tokens) if q_tokens else 0.0
        return "Relevant" if overlap >= 0.20 else "Irrelevant"

    def evaluate_support(self, response: str, context: str) -> str:
        r_tokens = set(re.findall(r"\b\w+\b", response.lower()))
        c_tokens = set(re.findall(r"\b\w+\b", context.lower()))

        if not r_tokens:
            return "Unsupported"

        support = len(r_tokens & c_tokens) / len(r_tokens)
        if support >= self.support_threshold:
            return "Fully Supported"
        elif support >= 0.30:
            return "Partially Supported"
        else:
            return "Unsupported"

    def evaluate_utility(self, response: str, query: str) -> int:
        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        r_tokens = set(re.findall(r"\b\w+\b", response.lower()))
        overlap = len(q_tokens & r_tokens) / len(q_tokens) if q_tokens else 0.0

        if overlap >= 0.6 and len(response.split()) >= 8:
            return 5
        elif overlap >= 0.4:
            return 4
        elif overlap >= 0.2:
            return 3
        return 2

    def reflect(self, query: str, context: str, response: str) -> Dict[str, Any]:
        retrieve_tag = self.evaluate_retrieval_need(query)
        rel_tag = self.evaluate_relevance(context, query)
        sup_tag = self.evaluate_support(response, context)
        use_tag = self.evaluate_utility(response, query)

        is_approved = (sup_tag in ["Fully Supported", "Partially Supported"]) and (use_tag >= 3)
        repaired = response if is_approved else self.auto_repair(response, context)

        return {
            "critique_tokens": {
                "[Retrieve]": retrieve_tag,
                "[IsRel]": rel_tag,
                "[IsSup]": sup_tag,
                "[IsUse]": use_tag,
            },
            "status": "APPROVED" if is_approved else "REJECTED_REPAIRED",
            "final_response": repaired,
        }

    def auto_repair(self, response: str, context: str) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", response.strip())
        c_tokens = set(re.findall(r"\b\w+\b", context.lower()))

        grounded = []
        for s in sentences:
            s_clean = s.strip()
            if not s_clean:
                continue
            s_tokens = set(re.findall(r"\b\w+\b", s_clean.lower()))
            overlap = len(s_tokens & c_tokens) / len(s_tokens) if s_tokens else 0.0
            if overlap >= 0.30:
                grounded.append(s_clean)

        return " ".join(grounded) if grounded else f"[Grounded Fact]: {context[:120]}..."
