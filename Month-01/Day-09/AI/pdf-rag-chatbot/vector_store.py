import chromadb
from embedding import embed_texts, embed_query

_client = chromadb.Client()
_collection = None

def get_collection(name: str = "pdf_rag"):
    global _collection
    if _collection is None:
        _collection = _client.get_or_create_collection(name)
    return _collection

def add_chunks(chunks: list[str], collection_name: str = "pdf_rag"):
    collection = get_collection(collection_name)
    embeddings = embed_texts(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f"✅ Indexed {len(chunks)} chunks.")

def search(query: str, n_results: int = 3, collection_name: str = "pdf_rag") -> list[str]:
    collection = get_collection(collection_name)
    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=n_results
    )
    return results["documents"][0]
