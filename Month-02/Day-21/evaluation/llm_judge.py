"""
llm_judge.py — LLM-as-a-Judge evaluator using Groq.
Scores responses on correctness, faithfulness, and helpfulness (1-5).
"""
import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

JUDGE_PROMPT = """You are an expert evaluator. Score the following AI response.

Question: {question}
Context: {context}
Expected Answer: {expected}
Actual Response: {prediction}

Rate on these criteria (1-5 each):
- correctness: Is the answer factually correct?
- faithfulness: Is it grounded in the context?
- helpfulness: Is it clear and useful?

Respond ONLY with valid JSON:
{{"correctness": <1-5>, "faithfulness": <1-5>, "helpfulness": <1-5>, "reasoning": "<one sentence>"}}"""


def llm_judge(question: str, context: str, expected: str, prediction: str) -> dict:
    prompt = JUDGE_PROMPT.format(
        question=question, context=context,
        expected=expected, prediction=prediction
    )
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"correctness": 0, "faithfulness": 0, "helpfulness": 0, "reasoning": str(e)}


def batch_llm_judge(samples: list) -> dict:
    results = []
    for s in samples:
        score = llm_judge(s["question"], s["context"], s["expected"], s["prediction"])
        results.append(score)
    avg = lambda key: round(sum(r[key] for r in results) / len(results), 4)
    return {
        "avg_correctness": avg("correctness"),
        "avg_faithfulness": avg("faithfulness"),
        "avg_helpfulness": avg("helpfulness"),
        "individual": results,
    }
