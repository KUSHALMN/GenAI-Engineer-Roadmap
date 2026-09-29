"""
Day 21 AI — RAG Pipeline with built-in evaluation scoring
Retrieves context from a mock store, generates answer, evaluates quality.
"""
import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# ── Mock Knowledge Base ────────────────────────────────────────────────────────

KNOWLEDGE_BASE = [
    {"id": 1, "text": "RAG (Retrieval-Augmented Generation) combines a retriever with a generator LLM to produce grounded, factual answers by fetching relevant documents before generation."},
    {"id": 2, "text": "LoRA (Low-Rank Adaptation) is a PEFT method that injects trainable low-rank matrices into transformer attention layers, reducing trainable parameters by 99%."},
    {"id": 3, "text": "Vector databases store high-dimensional embeddings and support approximate nearest neighbor (ANN) search using algorithms like HNSW and IVF."},
    {"id": 4, "text": "Prompt injection is an attack where malicious user input overrides the system prompt, causing the LLM to ignore safety instructions."},
    {"id": 5, "text": "Temperature in LLMs controls output randomness by scaling logits before softmax. Low temperature = deterministic; high temperature = creative."},
]

# ── Simple Keyword Retriever ───────────────────────────────────────────────────

def retrieve(query: str, top_k: int = 2) -> list:
    query_tokens = set(re.findall(r"\w+", query.lower()))
    scored = []
    for doc in KNOWLEDGE_BASE:
        doc_tokens = set(re.findall(r"\w+", doc["text"].lower()))
        score = len(query_tokens & doc_tokens) / len(query_tokens) if query_tokens else 0
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]

# ── Generator ─────────────────────────────────────────────────────────────────

def generate(query: str, context_docs: list) -> str:
    if not os.getenv("GROQ_API_KEY"):
        # Fallback extractive generation when API key is not configured
        if not context_docs:
            return "No relevant context found."
        return context_docs[0]["text"]

    context = "\n".join(f"- {d['text']}" for d in context_docs)
    prompt = f"""Answer the question using ONLY the context below.

Context:
{context}

Question: {query}
Answer:"""
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during generation: {e}"

# ── Faithfulness Check ─────────────────────────────────────────────────────────

def faithfulness_score(answer: str, context_docs: list) -> float:
    ctx_tokens = set(re.findall(r"\w+", " ".join(d["text"] for d in context_docs).lower()))
    ans_tokens = set(re.findall(r"\w+", answer.lower()))
    if not ans_tokens:
        return 0.0
    return round(len(ans_tokens & ctx_tokens) / len(ans_tokens), 4)

# ── RAG Pipeline ──────────────────────────────────────────────────────────────

def rag_pipeline(query: str) -> dict:
    docs    = retrieve(query)
    answer  = generate(query, docs)
    faith   = faithfulness_score(answer, docs)
    return {
        "query":       query,
        "answer":      answer,
        "faithfulness": faith,
        "retrieved":   [d["id"] for d in docs],
    }

if __name__ == "__main__":
    queries = [
        "What is RAG?",
        "How does LoRA work?",
        "What is a vector database?",
    ]
    for q in queries:
        result = rag_pipeline(q)
        print(f"\nQ: {result['query']}")
        print(f"A: {result['answer'][:120]}...")
        print(f"Faithfulness: {result['faithfulness']}")
