import chromadb
from embedding import embed_texts, embed_query
from config import COLLECTION_NAME

_client = chromadb.Client()
_collection = None

def get_collection(name: str = COLLECTION_NAME):
    global _collection
    if _collection is None:
        _collection = _client.get_or_create_collection(name)
    return _collection

def add_chunks(chunks: list[str]):
    collection = get_collection()
    embeddings = embed_texts(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f"✅ Indexed {len(chunks)} chunks.")

def search(query: str, n_results: int = 3) -> list[str]:
    results = get_collection().query(
        query_embeddings=[embed_query(query)],
        n_results=n_results
    )
    return results["documents"][0]
