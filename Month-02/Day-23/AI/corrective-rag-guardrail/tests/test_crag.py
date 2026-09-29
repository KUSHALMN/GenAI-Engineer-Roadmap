import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from core.retrieval_evaluator import RetrievalEvaluator
from core.knowledge_refiner import KnowledgeRefiner
from core.query_transformer import QueryTransformer
from core.self_rag_guardrail import SelfRAGGuardrail
from app.crag_engine import CRAGEngine


def test_retrieval_evaluator():
    evaluator = RetrievalEvaluator()
    docs = [{"title": "LoRA Fine Tuning", "content": "LoRA freezes weights and adds rank matrices."}]

    action, conf = evaluator.evaluate("How does LoRA work?", docs)
    assert action in ["CORRECT", "AMBIGUOUS"]
    assert conf > 0.0

    action_empty, conf_empty = evaluator.evaluate("Quantum encryption", [])
    assert action_empty == "INCORRECT"
    assert conf_empty == 0.0


def test_knowledge_refiner():
    refiner = KnowledgeRefiner()
    docs = [{
        "title": "LoRA",
        "content": "LoRA reduces memory. Baking sourdough requires flour and yeast."
    }]
    strips = refiner.refine(docs, "memory reduction with LoRA")
    assert any("reduces memory" in s for s in strips)
    assert not any("sourdough" in s for s in strips)


def test_query_transformer():
    qt = QueryTransformer()
    rewritten = qt.rewrite("how to use lora and mcp")
    assert "low-rank adaptation" in rewritten
    assert "model context protocol" in rewritten

    web_results = qt.web_search("quantum computing")
    assert len(web_results) > 0


def test_self_rag_guardrail():
    guardrail = SelfRAGGuardrail()
    query = "What is LoRA?"
    context = "LoRA is Low Rank Adaptation."
    supported_ans = "LoRA stands for Low Rank Adaptation."

    result = guardrail.reflect(query, context, supported_ans)
    assert result["critique_tokens"]["[Retrieve]"] == "Yes"
    assert result["critique_tokens"]["[IsSup]"] in ["Fully Supported", "Partially Supported"]
    assert result["status"] == "APPROVED"


def test_crag_engine_pipeline():
    engine = CRAGEngine()
    res = engine.query("What are the benefits of LoRA?")
    assert "decision" in res
    assert "reflection" in res
    assert len(res["response"]) > 0
