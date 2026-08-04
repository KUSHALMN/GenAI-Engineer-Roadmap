from vector_store import search

def retrieve(query: str, n_results: int = 3) -> list[str]:
    """Retrieve top-n relevant chunks for a given query."""
    return search(query, n_results=n_results)

def retrieve_with_scores(query: str, n_results: int = 3) -> list[dict]:
    """Retrieve chunks with their similarity metadata."""
    from embedding import embed_query
    from vector_store import get_collection

    collection = get_collection()
    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=n_results,
        include=["documents", "distances"]
    )
    chunks = results["documents"][0]
    distances = results["distances"][0]

    return [
        {"chunk": chunk, "distance": round(dist, 4)}
        for chunk, dist in zip(chunks, distances)
    ]
