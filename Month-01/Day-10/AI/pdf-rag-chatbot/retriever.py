from vector_store import search, get_collection
from embedding import embed_query

def retrieve(query: str, n_results: int = 3) -> list[str]:
    return search(query, n_results=n_results)

def retrieve_with_scores(query: str, n_results: int = 3) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=n_results,
        include=["documents", "distances"]
    )
    return [
        {"chunk": chunk, "distance": round(dist, 4)}
        for chunk, dist in zip(results["documents"][0], results["distances"][0])
    ]
