from app.splitter import split_text
from app.prompt_builder import build_prompt
from retrieval.keyword_retriever import keyword_retrieve


def test_split_returns_chunks():
    chunks = split_text("a" * 1200)
    assert len(chunks) > 1


def test_build_prompt_contains_question():
    prompt = build_prompt("What is RAG?", ["RAG is Retrieval-Augmented Generation."])
    assert "What is RAG?" in prompt
    assert "Context:" in prompt


def test_keyword_retrieve_empty():
    results = keyword_retrieve("nonexistent query xyz")
    assert isinstance(results, list)
