from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.source_handler import load_and_chunk
from app.retriever import store, retrieve
from app.prompt_builder import build_prompt

client = Groq(api_key=GROQ_API_KEY)


def ingest(pdf_path: str):
    chunks = load_and_chunk(pdf_path)
    store(chunks)
    print(f"Ingested {len(chunks)} chunks.")


def query(question: str) -> str:
    chunks = retrieve(question)
    prompt = build_prompt(question, chunks)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
