from groq import Groq
from retriever import retrieve
from prompt_builder import build_prompt
from config import GROQ_API_KEY, LLM_MODEL, N_RESULTS

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def run_chain(question: str, n_results: int = N_RESULTS) -> dict:
    context_chunks = retrieve(question, n_results=n_results)
    messages = build_prompt(question, context_chunks)
    response = get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )
    return {
        "question": question,
        "context": context_chunks,
        "answer": response.choices[0].message.content
    }
