from app.splitter import split_text


def test_split_returns_chunks():
    chunks = split_text("a" * 1200)
    assert len(chunks) > 1


def test_chunk_size_respected():
    chunks = split_text("b" * 1200)
    assert all(len(c) <= 500 for c in chunks)
