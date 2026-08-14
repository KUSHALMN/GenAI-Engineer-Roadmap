from retrieval.hybrid_retriever import hybrid_retrieve


def retrieve(question: str) -> list[str]:
    return hybrid_retrieve(question)
