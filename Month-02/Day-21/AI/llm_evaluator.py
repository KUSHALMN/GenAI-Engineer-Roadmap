"""
Day 21 AI — LLM Evaluation Pipeline
Topic: Rule-based eval, Token F1, LLM-as-Judge with Groq
"""
import os
import re
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# ── Metrics ────────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", "", re.sub(r"\s+", " ", text.lower().strip()))

def exact_match(pred: str, expected: str) -> float:
    return float(normalize(pred) == normalize(expected))

def token_f1(pred: str, expected: str) -> float:
    p = set(re.findall(r"\w+", pred.lower()))
    e = set(re.findall(r"\w+", expected.lower()))
    if not p or not e:
        return 0.0
    precision = len(p & e) / len(p)
    recall    = len(p & e) / len(e)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)

# ── LLM Judge ─────────────────────────────────────────────────────────────────

JUDGE_PROMPT = """You are an expert evaluator. Score the AI response below.

Question: {question}
Expected: {expected}
Prediction: {prediction}

Return ONLY valid JSON:
{{"correctness": <1-5>, "helpfulness": <1-5>, "reasoning": "<one sentence>"}}"""

def llm_judge(question: str, expected: str, prediction: str) -> dict:
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": JUDGE_PROMPT.format(
                question=question, expected=expected, prediction=prediction
            )}],
            temperature=0.0,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"correctness": 0, "helpfulness": 0, "reasoning": str(e)}

# ── Evaluator ─────────────────────────────────────────────────────────────────

SAMPLES = [
    {
        "question": "What is RAG?",
        "expected": "RAG combines retrieval with generation to produce grounded answers.",
        "prediction": "RAG stands for Retrieval-Augmented Generation, combining a retriever and a generator LLM.",
    },
    {
        "question": "What is LoRA?",
        "expected": "LoRA is a parameter-efficient fine-tuning method using low-rank matrices.",
        "prediction": "LoRA injects trainable low-rank matrices into transformer layers for efficient fine-tuning.",
    },
    {
        "question": "What is a vector database?",
        "expected": "A vector database stores embeddings and enables fast similarity search.",
        "prediction": "A vector database stores high-dimensional embeddings and supports ANN similarity search.",
    },
]

def run_evaluation(use_llm_judge: bool = False) -> dict:
    results = []
    for s in SAMPLES:
        em  = exact_match(s["prediction"], s["expected"])
        f1  = token_f1(s["prediction"], s["expected"])
        row = {"question": s["question"], "exact_match": em, "token_f1": f1}
        if use_llm_judge:
            row["llm_judge"] = llm_judge(s["question"], s["expected"], s["prediction"])
        results.append(row)

    avg_em = round(sum(r["exact_match"] for r in results) / len(results), 4)
    avg_f1 = round(sum(r["token_f1"]    for r in results) / len(results), 4)

    report = {"samples": len(results), "avg_exact_match": avg_em, "avg_token_f1": avg_f1, "results": results}
    print(f"Samples:        {report['samples']}")
    print(f"Avg Exact Match:{avg_em}")
    print(f"Avg Token F1:   {avg_f1}")
    return report

if __name__ == "__main__":
    run_evaluation(use_llm_judge=False)
