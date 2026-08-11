from app.splitter import split_text
from app.prompt_builder import build_prompt


def test_split_text():
    chunks = split_text("a" * 1200)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)


def test_build_prompt():
    prompt = build_prompt("What is RAG?", ["RAG stands for Retrieval-Augmented Generation."])
    assert "RAG" in prompt
    assert "Question:" in prompt
