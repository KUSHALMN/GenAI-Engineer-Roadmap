import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from core.metrics import exact_match, normalized_exact_match, token_f1, compute_lexical_metrics
from core.llm_judge import evaluate_with_llm_judge


def test_exact_match():
    assert exact_match("Hello world", "Hello world") == 1.0
    assert exact_match("Hello world", "hello world") == 0.0


def test_normalized_exact_match():
    assert normalized_exact_match("The quick brown fox.", "quick brown fox") == 1.0
    assert normalized_exact_match("A Dog!", "dog") == 1.0


def test_token_f1():
    pred = "RAG combines retrieval and generation"
    truth = "RAG combines retrieval with generation"
    res = token_f1(pred, truth)
    assert res["f1"] > 0.70
    assert res["precision"] > 0.70
    assert res["recall"] > 0.70


def test_compute_lexical_metrics():
    metrics = compute_lexical_metrics("LoRA fine-tuning", "LoRA fine-tuning")
    assert metrics["exact_match"] == 1.0
    assert metrics["f1"] == 1.0


def test_llm_judge_mock():
    res = evaluate_with_llm_judge(
        question="What is LoRA?",
        context="LoRA is parameter-efficient fine-tuning.",
        expected="LoRA fine-tunes with fewer parameters.",
        prediction="LoRA is efficient fine-tuning."
    )
    assert "correctness" in res
    assert "faithfulness" in res
    assert res["correctness"] >= 1
