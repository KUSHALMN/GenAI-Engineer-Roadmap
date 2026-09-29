"""
app/crag_engine.py — Core CRAG Orchestrator
Executes: Document Retrieval -> Quality Evaluation -> (Refine / Fallback) -> Synthesis
"""
import os
import re
import json
from typing import List, Dict, Any

from core.retrieval_evaluator import RetrievalEvaluator
from core.knowledge_refiner import KnowledgeRefiner
from core.query_transformer import QueryTransformer
from core.self_rag_guardrail import SelfRAGGuardrail
from app.config import settings


class CRAGEngine:
    def __init__(self, data_path: str = "data/knowledge_base.json"):
        if not os.path.exists(data_path):
            base = os.path.dirname(os.path.dirname(__file__))
            data_path = os.path.join(base, "data", "knowledge_base.json")

        with open(data_path, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

        self.evaluator = RetrievalEvaluator(
            upper_threshold=settings.upper_confidence_threshold,
            lower_threshold=settings.lower_confidence_threshold
        )
        self.refiner = KnowledgeRefiner()
        self.transformer = QueryTransformer()
        self.guardrail = SelfRAGGuardrail(support_threshold=settings.support_threshold)

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        scored = []
        for d in self.docs:
            d_tokens = set(re.findall(r"\b\w+\b", (d["title"] + " " + d["content"]).lower()))
            overlap = len(q_tokens & d_tokens) / len(q_tokens) if q_tokens else 0.0
            scored.append((overlap, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored[:top_k] if score > 0]

    def query(self, user_query: str) -> Dict[str, Any]:
        docs = self.retrieve(user_query)
        action, conf = self.evaluator.evaluate(user_query, docs)

        knowledge_strips = []
        fallback_used = False

        if action == "CORRECT":
            knowledge_strips = self.refiner.refine(docs, user_query)
        elif action == "AMBIGUOUS":
            knowledge_strips = self.refiner.refine(docs, user_query)
            knowledge_strips.extend(self.transformer.web_search(user_query))
            fallback_used = True
        else:
            rewritten = self.transformer.rewrite(user_query)
            knowledge_strips = self.transformer.web_search(rewritten)
            fallback_used = True

        synthesized = " ".join(knowledge_strips) if knowledge_strips else "No knowledge available."
        reflection = self.guardrail.reflect(user_query, synthesized, synthesized)

        return {
            "query": user_query,
            "decision": action,
            "confidence": conf,
            "fallback_used": fallback_used,
            "retrieved_docs": len(docs),
            "knowledge_strips": len(knowledge_strips),
            "reflection": reflection["critique_tokens"],
            "response": reflection["final_response"],
        }
