"""
Day 23 AI — Corrective RAG (CRAG) Pipeline
Implements retrieval evaluation, knowledge refinement (striping), and query fallback.
"""
import os
import re
from typing import List, Dict, Any, Tuple


class DocumentStore:
    def __init__(self):
        self.docs = [
            {
                "id": "doc-1",
                "title": "Low-Rank Adaptation (LoRA)",
                "content": "LoRA freezes the pre-trained model weights and injects trainable rank decomposition matrices into each transformer layer, reducing trainable parameters by up to 10,000x and GPU memory requirements by 3x."
            },
            {
                "id": "doc-2",
                "title": "Quantized Low-Rank Adaptation (QLoRA)",
                "content": "QLoRA backpropagates gradients through a frozen, 4-bit quantized pre-trained language model into Low Rank Adapters (LoRA), utilizing NormalFloat4 (NF4) data types and double quantization."
            },
            {
                "id": "doc-3",
                "title": "Model Context Protocol (MCP)",
                "content": "Model Context Protocol is an open standard that enables AI models to securely connect to external tools, data sources, and services using standardized JSON-RPC client-server primitives."
            },
            {
                "id": "doc-4",
                "title": "Unrelated Cooking Recipes",
                "content": "To make sourdough bread, mix flour, water, salt, and active sourdough starter. Ferment for 12 hours before baking in a Dutch oven at 450F."
            }
        ]

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        q_tokens = set(re.findall(r"\w+", query.lower()))
        scored = []
        for d in self.docs:
            d_tokens = set(re.findall(r"\w+", (d["title"] + " " + d["content"]).lower()))
            overlap = len(q_tokens & d_tokens) / len(q_tokens) if q_tokens else 0.0
            scored.append((overlap, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored[:top_k] if score > 0]


class RetrievalEvaluator:
    """
    Evaluates retrieved documents against the query to categorize confidence:
    - CORRECT: High confidence, proceed with knowledge refinement
    - AMBIGUOUS: Moderate confidence, combine refined knowledge with web search/query rewrite
    - INCORRECT: Low confidence, discard retrieved docs and trigger web search/query transformation
    """

    def __init__(self, upper_threshold: float = 0.35, lower_threshold: float = 0.15):
        self.upper = upper_threshold
        self.lower = lower_threshold

    def evaluate(self, query: str, docs: List[Dict[str, str]]) -> Tuple[str, float]:
        if not docs:
            return "INCORRECT", 0.0

        q_tokens = set(re.findall(r"\w+", query.lower()))
        scores = []
        for d in docs:
            full_text = (d.get("title", "") + " " + d.get("content", "")).lower()
            c_tokens = set(re.findall(r"\w+", full_text))
            score = len(q_tokens & c_tokens) / len(q_tokens) if q_tokens else 0.0
            scores.append(score)

        avg_score = sum(scores) / len(scores)

        if avg_score >= self.upper:
            return "CORRECT", round(avg_score, 4)
        elif avg_score >= self.lower:
            return "AMBIGUOUS", round(avg_score, 4)
        else:
            return "INCORRECT", round(avg_score, 4)


class KnowledgeRefiner:
    """
    Decomposes documents into fine-grained knowledge strips (sentences)
    and filters out irrelevant noise.
    """

    @staticmethod
    def refine(docs: List[Dict[str, str]], query: str) -> List[str]:
        q_tokens = set(re.findall(r"\w+", query.lower()))
        refined_strips = []

        for doc in docs:
            sentences = re.split(r"(?<=[.!?])\s+", doc["content"])
            for s in sentences:
                s_tokens = set(re.findall(r"\w+", s.lower()))
                if len(q_tokens & s_tokens) > 0:
                    refined_strips.append(s.strip())

        return refined_strips


class CorrectiveRAG:
    """
    Complete CRAG pipeline executing:
    Retrieval -> Evaluation -> (Refine | Web Fallback | Query Rewrite) -> Generation
    """

    def __init__(self):
        self.store = DocumentStore()
        self.evaluator = RetrievalEvaluator()
        self.refiner = KnowledgeRefiner()

    def mock_web_search(self, query: str) -> List[str]:
        """Fallback web search simulator for ambiguous or out-of-domain queries."""
        return [f"[Web Result] Up-to-date documentation on '{query}' fetched via search API."]

    def rewrite_query(self, query: str) -> str:
        """Query re-writing to expand synonyms and improve retrieval."""
        synonyms = {"lora": "low-rank adaptation", "mcp": "model context protocol"}
        rewritten = query.lower()
        for k, v in synonyms.items():
            if k in rewritten:
                rewritten = rewritten.replace(k, f"{k} ({v})")
        return rewritten

    def run(self, query: str) -> Dict[str, Any]:
        docs = self.store.search(query)
        action, conf = self.evaluator.evaluate(query, docs)

        knowledge_base = []
        fallback_used = False

        if action == "CORRECT":
            knowledge_base = self.refiner.refine(docs, query)
        elif action == "AMBIGUOUS":
            # Combine refined docs with web search
            knowledge_base = self.refiner.refine(docs, query)
            knowledge_base.extend(self.mock_web_search(query))
            fallback_used = True
        else: # INCORRECT
            rewritten = self.rewrite_query(query)
            knowledge_base = self.mock_web_search(rewritten)
            fallback_used = True

        answer = " ".join(knowledge_base) if knowledge_base else "No sufficient knowledge found."

        return {
            "query": query,
            "decision": action,
            "confidence": conf,
            "retrieved_doc_count": len(docs),
            "fallback_used": fallback_used,
            "knowledge_strips": len(knowledge_base),
            "final_context": answer[:150] + ("..." if len(answer) > 150 else "")
        }


if __name__ == "__main__":
    crag = CorrectiveRAG()
    test_queries = [
        "What are the benefits of LoRA parameter reduction?",
        "How does MCP enable tool calling?",
        "What is the latest quantum computing algorithm for LLMs?",
    ]

    print("=" * 65)
    print("[RUN] Corrective RAG (CRAG) Self-Correction Pipeline")
    print("=" * 65)

    for q in test_queries:
        res = crag.run(q)
        print(f"\nQuery:      '{res['query']}'")
        print(f"Decision:   {res['decision']} (Confidence: {res['confidence']})")
        print(f"Fallback:   {res['fallback_used']} (Strips: {res['knowledge_strips']})")
        print(f"Synthesis:  {res['final_context']}")
