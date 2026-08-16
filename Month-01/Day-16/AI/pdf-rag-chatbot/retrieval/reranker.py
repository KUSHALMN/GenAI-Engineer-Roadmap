from app.config import TOP_K


def rerank(question: str, chunks: list[str]) -> list[str]:
    """
    Re-scores candidate chunks against the query.
    Uses term frequency overlap as a lightweight cross-encoder proxy.
    Replace scoring logic with a cross-encoder model for production.
    """
    query_terms = set(question.lower().split())

    scored = []
    for chunk in chunks:
        chunk_terms = chunk.lower().split()
        term_freq = sum(chunk_terms.count(t) for t in query_terms)
        coverage = len(query_terms & set(chunk_terms))
        score = term_freq + coverage * 2  # coverage weighted higher
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:TOP_K]]
