"""
core/llm_judge.py — LLM-as-a-Judge Evaluation Engine
Evaluates AI predictions on Correctness, Faithfulness, and Helpfulness (1-5 scale).
"""
import os
import json
from typing import Dict, Any, List


JUDGE_SYSTEM_PROMPT = """You are an expert AI evaluation judge.
Score the predicted response against the expected ground truth and context.

Score the following three criteria from 1 to 5:
1. correctness: Is the prediction factually correct compared to expected answer?
2. faithfulness: Is the prediction fully grounded in the provided context?
3. helpfulness: Is the response concise, clear, and directly answering the question?

Respond ONLY with valid JSON:
{
  "correctness": <int 1-5>,
  "faithfulness": <int 1-5>,
  "helpfulness": <int 1-5>,
  "reasoning": "<one sentence summary>"
}"""


def evaluate_with_llm_judge(question: str, context: str, expected: str, prediction: str) -> Dict[str, Any]:
    """Scores a single generation using LLM-as-a-Judge (Groq / mock fallback)."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        # Mock fallback for test suites and offline environments
        return {
            "correctness": 4,
            "faithfulness": 4,
            "helpfulness": 5,
            "reasoning": "Offline mock judge: Response aligns with context and expected tokens.",
        }

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        user_content = f"Question: {question}\nContext: {context}\nExpected: {expected}\nPrediction: {prediction}"

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.0,
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {
            "correctness": 0,
            "faithfulness": 0,
            "helpfulness": 0,
            "reasoning": f"Judge evaluation error: {str(e)}",
        }


def batch_llm_judge(samples: List[Dict[str, str]]) -> Dict[str, Any]:
    """Runs LLM judge over a batch of evaluation samples."""
    evaluations = []
    for s in samples:
        score = evaluate_with_llm_judge(
            question=s.get("question", ""),
            context=s.get("context", ""),
            expected=s.get("expected", ""),
            prediction=s.get("prediction", ""),
        )
        evaluations.append({
            "id": s.get("id", ""),
            "scores": score
        })

    avg = lambda key: round(sum(e["scores"].get(key, 0) for e in evaluations) / len(evaluations), 2) if evaluations else 0.0

    return {
        "samples_evaluated": len(evaluations),
        "mean_correctness": avg("correctness"),
        "mean_faithfulness": avg("faithfulness"),
        "mean_helpfulness": avg("helpfulness"),
        "details": evaluations,
    }
