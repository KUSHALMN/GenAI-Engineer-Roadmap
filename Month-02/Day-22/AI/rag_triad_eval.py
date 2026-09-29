"""
Day 22 AI — Advanced RAG Evaluation: RAG Triad
Measures Context Relevance, Faithfulness, and Answer Relevance.
"""
import os
import re
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# ── RAG Triad Metrics ──────────────────────────────────────────────────────────

def tokenize(text: str) -> set:
    return set(re.findall(r"\w+", text.lower()))

def context_relevance(question: str, context: str) -> float:
    """How much of the question is covered by the context."""
    q = tokenize(question)
    c = tokenize(context)
    return round(len(q & c) / len(q), 4) if q else 0.0

def faithfulness(answer: str, context: str) -> float:
    """How much of the answer is grounded in the context."""
    a = tokenize(answer)
    c = tokenize(context)
    return round(len(a & c) / len(a), 4) if a else 0.0

def answer_relevance(answer: str, question: str) -> float:
    """How much of the question vocabulary appears in the answer."""
    a = tokenize(answer)
    q = tokenize(question)
    return round(len(a & q) / len(q), 4) if q else 0.0

def rag_triad_score(question: str, context: str, answer: str) -> dict:
    cr = context_relevance(question, context)
    fa = faithfulness(answer, context)
    ar = answer_relevance(answer, question)
    return {
        "context_relevance": cr,
        "faithfulness":      fa,
        "answer_relevance":  ar,
        "overall":           round((cr + fa + ar) / 3, 4),
    }

# ── LLM RAG Triad Judge ────────────────────────────────────────────────────────

TRIAD_PROMPT = """Evaluate this RAG response on 3 dimensions (score 1-5 each).

Question: {question}
Context: {context}
Answer: {answer}

Return ONLY valid JSON:
{{"context_relevance": <1-5>, "faithfulness": <1-5>, "answer_relevance": <1-5>, "reasoning": "<one sentence>"}}"""

def llm_rag_triad(question: str, context: str, answer: str) -> dict:
    if not os.getenv("GROQ_API_KEY"):
        return {"context_relevance": 4, "faithfulness": 4, "answer_relevance": 4, "reasoning": "Mock evaluation (GROQ_API_KEY not set)"}
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": TRIAD_PROMPT.format(
                question=question, context=context, answer=answer
            )}],
            temperature=0.0,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"context_relevance": 0, "faithfulness": 0, "answer_relevance": 0, "reasoning": str(e)}

# ── Batch Evaluation ──────────────────────────────────────────────────────────

SAMPLES = [
    {
        "question": "What is hybrid search?",
        "context":  "Hybrid search combines dense vector search with BM25 keyword search. Results are merged using Reciprocal Rank Fusion (RRF).",
        "answer":   "Hybrid search combines vector similarity and BM25 keyword search, merging results with RRF for better retrieval.",
    },
    {
        "question": "What is a reranker?",
        "context":  "A reranker is a cross-encoder model that scores query-document pairs and reorders retrieved candidates by relevance.",
        "answer":   "A reranker uses a cross-encoder to score and reorder retrieved documents based on query relevance.",
    },
    {
        "question": "What is HyDE?",
        "context":  "HyDE generates a hypothetical answer using an LLM, then embeds it to retrieve similar real documents.",
        "answer":   "HyDE generates a hypothetical document with an LLM and retrieves real documents similar to its embedding.",
    },
]

def run_rag_triad_evaluation() -> dict:
    results = [rag_triad_score(s["question"], s["context"], s["answer"]) for s in SAMPLES]
    avg = lambda k: round(sum(r[k] for r in results) / len(results), 4)
    report = {
        "samples": len(results),
        "avg_context_relevance": avg("context_relevance"),
        "avg_faithfulness":      avg("faithfulness"),
        "avg_answer_relevance":  avg("answer_relevance"),
        "avg_overall":           avg("overall"),
        "results":               results,
    }
    print(f"Samples:               {report['samples']}")
    print(f"Avg Context Relevance: {report['avg_context_relevance']}")
    print(f"Avg Faithfulness:      {report['avg_faithfulness']}")
    print(f"Avg Answer Relevance:  {report['avg_answer_relevance']}")
    print(f"Avg Overall:           {report['avg_overall']}")
    return report

if __name__ == "__main__":
    run_rag_triad_evaluation()
