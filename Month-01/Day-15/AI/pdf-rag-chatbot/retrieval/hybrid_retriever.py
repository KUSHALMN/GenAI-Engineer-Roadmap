from retrieval.semantic_retriever import semantic_retrieve
from retrieval.keyword_retriever import keyword_retrieve
from app.config import TOP_K


def hybrid_retrieve(question: str) -> list[str]:
    semantic = semantic_retrieve(question)
    keyword = keyword_retrieve(question)

    # merge, deduplicate, preserve order
    seen, merged = set(), []
    for chunk in semantic + keyword:
        if chunk not in seen:
            seen.add(chunk)
            merged.append(chunk)

    return merged[:TOP_K]
