import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

def load_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks

def build_vector_store(chunks, collection_name="pdf_store"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.Client()
    collection = client.create_collection(collection_name)

    embeddings = model.encode(chunks).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk{i}" for i in range(len(chunks))]
    )
    return collection, model

def search(collection, model, query, n_results=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results['documents'][0]

# --- Main ---
# Replace with your actual PDF path
PDF_PATH = "sample.pdf"

# For demo, create a dummy text instead of a real PDF
sample_chunks = [
    "RAG stands for Retrieval Augmented Generation.",
    "ChromaDB is a vector database used for semantic search.",
    "Embeddings convert text into numerical vectors.",
    "LangChain helps build LLM-powered applications.",
    "FastAPI is used to build REST APIs in Python.",
]

collection, model = build_vector_store(sample_chunks)

query = "What is a vector database?"
results = search(collection, model, query)

print(f"Query: {query}\n")
for i, doc in enumerate(results):
    print(f"  Result {i+1}: {doc}")
