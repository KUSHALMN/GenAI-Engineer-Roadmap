import os
from groq import Groq
from dotenv import load_dotenv
from retriever import retrieve
from prompt_builder import build_prompt

load_dotenv()
_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

def run_chain(question: str, n_results: int = 3, model: str = "llama-3.3-70b-versatile") -> dict:
    """
    Full RAG chain:
    question → retrieve context → build prompt → LLM → answer
    Returns dict with question, context, and answer.
    """
    context_chunks = retrieve(question, n_results=n_results)
    messages = build_prompt(question, context_chunks)

    response = get_client().chat.completions.create(
        model=model,
        messages=messages
    )
    answer = response.choices[0].message.content

    return {
        "question": question,
        "context": context_chunks,
        "answer": answer
    }
