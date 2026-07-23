import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("day2_demo")

docs = [
    "LangChain is a framework for building LLM applications.",
    "ChromaDB is an open-source vector database.",
    "FastAPI is a modern Python web framework.",
    "Docker helps containerize applications.",
]

embeddings = model.encode(docs).tolist()

collection.add(
    documents=docs,
    embeddings=embeddings,
    ids=[f"doc{i}" for i in range(len(docs))]
)

query = "What is a vector database?"
query_embedding = model.encode(query).tolist()

results = collection.query(query_embeddings=[query_embedding], n_results=2)
print(f"Query: {query}\n")
for doc in results['documents'][0]:
    print(f"  → {doc}")
