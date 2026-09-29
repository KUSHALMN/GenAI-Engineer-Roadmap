"""
llm_judge.py — RAG Triad LLM Judge: context relevance, faithfulness, answer relevance.
"""
import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

RAG_TRIAD_PROMPT = """You are an expert RAG evaluator. Evaluate the following:

Question: {question}
Retrieved Context: {context}
Generated Answer: {prediction}

Score each dimension (1-5):
- context_relevance: Is the context relevant to the question?
- faithfulness: Is the answer fully supported by the context?
- answer_relevance: Does the answer address the question?

Respond ONLY with valid JSON:
{{"context_relevance": <1-5>, "faithfulness": <1-5>, "answer_relevance": <1-5>, "reasoning": "<one sentence>"}}"""


def rag_triad_judge(question: str, context: str, prediction: str) -> dict:
    prompt = RAG_TRIAD_PROMPT.format(
        question=question, context=context, prediction=prediction
    )
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"context_relevance": 0, "faithfulness": 0, "answer_relevance": 0, "reasoning": str(e)}


def batch_rag_triad(samples: list) -> dict:
    results = [rag_triad_judge(s["question"], s["context"], s["prediction"]) for s in samples]
    avg = lambda k: round(sum(r[k] for r in results) / len(results), 4)
    return {
        "avg_context_relevance": avg("context_relevance"),
        "avg_faithfulness": avg("faithfulness"),
        "avg_answer_relevance": avg("answer_relevance"),
        "individual": results,
    }
