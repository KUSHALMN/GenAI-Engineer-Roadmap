"""
core/llm_judge.py — LLM-as-a-Judge RAG Triad Evaluator
Uses Groq LLM (or mock fallback) to rate Context Relevance, Faithfulness, and Answer Relevance (1-5).
"""
import os
import json
from typing import Dict, Any, List

TRIAD_JUDGE_PROMPT = """You are an expert AI evaluator assessing a RAG response.
Evaluate the three core RAG Triad dimensions on a 1-5 integer scale:

1. context_relevance: Does the retrieved context contain the information needed to answer the question?
2. faithfulness: Is the answer completely grounded in the context without external or invented claims?
3. answer_relevance: Does the answer directly and fully address the user question?

Question: {question}
Context: {context}
Answer: {answer}

Return ONLY valid JSON:
{{
  "context_relevance": <int 1-5>,
  "faithfulness": <int 1-5>,
  "answer_relevance": <int 1-5>,
  "reasoning": "<one concise sentence>"
}}"""


def llm_rag_triad_judge(question: str, context: str, answer: str) -> Dict[str, Any]:
    """Scores RAG generation using LLM-as-a-Judge."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        return {
            "context_relevance": 4,
            "faithfulness": 4,
            "answer_relevance": 4,
            "reasoning": "Offline mock judge: Response is well-grounded in context.",
        }

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": TRIAD_JUDGE_PROMPT.format(
                question=question, context=context, answer=answer
            )}],
            temperature=0.0,
        )
        return json.loads(resp.choices[0].message.content.strip())
    except Exception as e:
        return {
            "context_relevance": 0,
            "faithfulness": 0,
            "answer_relevance": 0,
            "reasoning": f"Judge error: {str(e)}",
        }


def batch_rag_triad_judge(samples: List[Dict[str, str]]) -> Dict[str, Any]:
    results = []
    for s in samples:
        score = llm_rag_triad_judge(s["question"], s["context"], s.get("prediction", s.get("answer", "")))
        results.append({"id": s.get("id", ""), "scores": score})

    avg = lambda k: round(sum(r["scores"].get(k, 0) for r in results) / len(results), 2) if results else 0.0

    return {
        "samples_evaluated": len(results),
        "mean_context_relevance": avg("context_relevance"),
        "mean_faithfulness": avg("faithfulness"),
        "mean_answer_relevance": avg("answer_relevance"),
        "details": results,
    }
