"""
Day 23 AI — Self-RAG (Self-Reflective RAG) & Critique Guardrails
Implements dynamic reflection tokens [Retrieve], [IsRel], [IsSup], [IsUse] with auto-repair.
"""
import re
from typing import Dict, Any, List


class SelfRAGGuardrail:
    """
    Self-RAG Evaluator & Guardrail.
    Scores generation across:
    1. Retrieval Need: [Retrieve] -> Yes / No
    2. Passage Relevance: [IsRel] -> Relevant / Irrelevant
    3. Grounding / Faithfulness: [IsSup] -> Fully Supported / Partially Supported / Unsupported
    4. Utility / Completeness: [IsUse] -> 1 to 5 Score
    """

    def __init__(self, support_threshold: float = 0.6):
        self.support_threshold = support_threshold

    def evaluate_retrieval_need(self, query: str) -> str:
        """Determines if the query demands factual retrieval or is conversational."""
        factual_keywords = ["what", "how", "why", "difference", "explain", "architecture", "algorithm", "compare"]
        tokens = set(re.findall(r"\w+", query.lower()))
        needs_retrieval = any(k in tokens for k in factual_keywords)
        return "Yes" if needs_retrieval else "No"

    def evaluate_relevance(self, context: str, query: str) -> str:
        """Evaluates whether retrieved passages are relevant to the user query."""
        q_tokens = set(re.findall(r"\w+", query.lower()))
        c_tokens = set(re.findall(r"\w+", context.lower()))
        overlap = len(q_tokens & c_tokens) / len(q_tokens) if q_tokens else 0.0
        return "Relevant" if overlap >= 0.25 else "Irrelevant"

    def evaluate_support(self, response: str, context: str) -> str:
        """Evaluates if the response tokens are factually grounded in the context."""
        r_tokens = set(re.findall(r"\w+", response.lower()))
        c_tokens = set(re.findall(r"\w+", context.lower()))

        if not r_tokens:
            return "Unsupported"

        support_ratio = len(r_tokens & c_tokens) / len(r_tokens)
        if support_ratio >= self.support_threshold:
            return "Fully Supported"
        elif support_ratio >= 0.35:
            return "Partially Supported"
        else:
            return "Unsupported"

    def evaluate_utility(self, response: str, query: str) -> int:
        """Scores 1-5 utility based on query keyword coverage and response length."""
        q_tokens = set(re.findall(r"\w+", query.lower()))
        r_tokens = set(re.findall(r"\w+", response.lower()))
        overlap = len(q_tokens & r_tokens) / len(q_tokens) if q_tokens else 0.0

        if overlap >= 0.7 and len(response.split()) >= 10:
            return 5
        elif overlap >= 0.5:
            return 4
        elif overlap >= 0.3:
            return 3
        elif len(response.strip()) > 0:
            return 2
        return 1

    def self_reflect(self, query: str, context: str, response: str) -> Dict[str, Any]:
        """Runs the complete self-reflection token assessment."""
        retrieve_tag = self.evaluate_retrieval_need(query)
        rel_tag = self.evaluate_relevance(context, query)
        sup_tag = self.evaluate_support(response, context)
        use_tag = self.evaluate_utility(response, query)

        passed = (sup_tag in ["Fully Supported", "Partially Supported"]) and (use_tag >= 3)

        return {
            "critique_tokens": {
                "[Retrieve]": retrieve_tag,
                "[IsRel]": rel_tag,
                "[IsSup]": sup_tag,
                "[IsUse]": use_tag,
            },
            "guardrail_status": "APPROVED" if passed else "REJECTED_NEEDS_REPAIR",
            "repaired_response": response if passed else self.auto_repair(response, context)
        }

    def auto_repair(self, response: str, context: str) -> str:
        """Auto-repairs an unsupported response by stripping ungrounded sentences."""
        sentences = re.split(r"(?<=[.!?])\s+", response.strip())
        c_tokens = set(re.findall(r"\w+", context.lower()))

        grounded_sentences = []
        for s in sentences:
            s_tokens = set(re.findall(r"\w+", s.lower()))
            overlap = len(s_tokens & c_tokens) / len(s_tokens) if s_tokens else 0.0
            if overlap >= 0.35:
                grounded_sentences.append(s.strip())

        if grounded_sentences:
            return " ".join(grounded_sentences)
        return f"Grounding Notice: Context confirms: '{context[:100]}...'"


# ── Interactive / Demo Test Cases ───────────────────────────────────────────────

if __name__ == "__main__":
    guardrail = SelfRAGGuardrail()

    test_cases = [
        {
            "query": "How does LoRA reduce memory usage during fine-tuning?",
            "context": "LoRA freezes the base model and injects low-rank trainable matrices into transformer attention blocks, saving up to 75% GPU memory.",
            "response": "LoRA freezes the base model weights and inserts low-rank matrices into attention layers, reducing GPU memory by up to 75%.",
        },
        {
            "query": "Explain what Model Context Protocol provides.",
            "context": "Model Context Protocol standardizes how LLMs access external tools and data sources via JSON-RPC.",
            "response": "Model Context Protocol connects tools via JSON-RPC. It was created in 1995 and guarantees zero latency using optical fiber.",
        }
    ]

    print("=" * 65)
    print("[RUN] Self-RAG Reflection & Critique Guardrail Benchmark")
    print("=" * 65)

    for i, t in enumerate(test_cases, 1):
        result = guardrail.self_reflect(t["query"], t["context"], t["response"])
        print(f"\n--- Case {i} ---")
        print(f"Query:    {t['query']}")
        print(f"Critique: {result['critique_tokens']}")
        print(f"Status:   {result['guardrail_status']}")
        if result['guardrail_status'] != "APPROVED":
            print(f"Repaired: {result['repaired_response']}")
