from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.source_handler import load_and_chunk
from app.retriever import store, retrieve

client = Groq(api_key=GROQ_API_KEY)


def ingest(pdf_path: str):
    chunks = load_and_chunk(pdf_path)
    store(chunks)
    print(f"Ingested {len(chunks)} chunks from {pdf_path}")


def query(question: str) -> str:
    chunks = retrieve(question)
    context = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(chunks))
    prompt = f"""You are a helpful assistant. Answer using only the context below.

Context:
{context}

Question: {question}
Answer:"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
