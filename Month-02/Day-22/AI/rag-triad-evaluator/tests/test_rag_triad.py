import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from core.triad_metrics import context_relevance, faithfulness, answer_relevance, compute_rag_triad
from core.hallucination_detector import HallucinationDetector
from core.llm_judge import llm_rag_triad_judge


def test_context_relevance():
    q = "What is LoRA?"
    c = "LoRA is Low-Rank Adaptation for parameter efficient training."
    score = context_relevance(q, c)
    assert score > 0.30


def test_faithfulness():
    ans = "LoRA saves GPU memory"
    ctx = "LoRA saves GPU memory by freezing model weights"
    score = faithfulness(ans, ctx)
    assert score == 1.0


def test_answer_relevance():
    q = "How does HNSW work?"
    ans = "HNSW builds a hierarchical navigable small world graph"
    score = answer_relevance(ans, q)
    assert score > 0.20


def test_compute_rag_triad():
    res = compute_rag_triad(
        question="What is RAG?",
        context="RAG combines search retrieval with generative LLMs.",
        answer="RAG combines retrieval with LLMs to generate grounded answers."
    )
    assert "composite_score" in res
    assert res["composite_score"] > 0.40


def test_hallucination_detection():
    detector = HallucinationDetector()
    context = "BERT uses bidirectional transformer encoders to produce contextual representations."
    grounded_ans = "BERT uses bidirectional encoders for representations."
    hallucinated_ans = "BERT uses quantum neural circuits invented in 2029 by OpenAI."

    g_eval = detector.evaluate(grounded_ans, context)
    assert g_eval["is_safe"] is True
    assert g_eval["hallucination_score"] == 0.0

    h_eval = detector.evaluate(hallucinated_ans, context)
    assert h_eval["is_safe"] is False
    assert h_eval["hallucination_score"] > 0.0


def test_llm_triad_judge_mock():
    res = llm_rag_triad_judge(
        question="What is LoRA?",
        context="LoRA injects low-rank matrices.",
        answer="LoRA injects low-rank matrices into attention layers."
    )
    assert res["context_relevance"] >= 1
    assert res["faithfulness"] >= 1
    assert res["answer_relevance"] >= 1
