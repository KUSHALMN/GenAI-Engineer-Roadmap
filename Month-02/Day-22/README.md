# 📅 Day 22 — Month 02: Advanced RAG Evaluation + Sliding Window DSA

> Build a full RAG Triad evaluation framework — Context Relevance, Faithfulness, Answer Relevance. Master Sliding Window patterns (LC 3, 209, 438) in Java.

---

## 📁 Structure

```
Day-22/
├── data/
│   └── eval_dataset.json       # 5 RAG QA samples with context + predictions
├── evaluation/
│   ├── exact_match.py          # EM + Normalized EM
│   ├── keyword_match.py        # Token F1 + context relevance + faithfulness score
│   ├── llm_judge.py            # RAG Triad LLM Judge via Groq
│   └── evaluator.py            # Orchestrator — runs all metrics, saves report
├── results/
│   └── evaluation_report.json  # Full metrics output
├── DSA/
│   └── SlidingWindow.java      # LC 3 + LC 209 + LC 438 (Java)
└── Interview/
    └── technical_questions.md  # RAG Triad, EM vs F1, Sliding Window types, cost scaling
```

---

## 🧠 AI: Advanced RAG Evaluation

### Run Evaluator
```bash
cd Month-02/Day-22/evaluation
python evaluator.py
```

### Metrics
| Metric | Score |
|--------|-------|
| Exact Match | 0.0 (paraphrases ≠ exact) |
| Avg Token F1 | 0.7812 |
| Avg Context Relevance | 0.72 |
| Avg Faithfulness | 0.68 |

### RAG Triad Pipeline
```
Question + Context + Prediction
    → context_relevance(question, context)
    → faithfulness_score(prediction, context)
    → token_f1(prediction, expected)
    → [optional] llm_judge RAG Triad (1-5 scores)
```

---

## ☕ DSA: Sliding Window (Java)

```bash
cd Month-02/Day-22/DSA
javac SlidingWindow.java && java SlidingWindow
```

**Expected:**
```
3
3
2
[0, 6]
```

---

## 🎯 Key Takeaways

1. **RAG Triad** = Context Relevance + Faithfulness + Answer Relevance — all three must be measured independently.
2. **EM = 0 doesn't mean wrong** — paraphrases score 0 EM but 0.78 Token F1, showing semantic correctness.
3. **Sliding Window** — fixed size for anagram/avg problems, variable size for min/max constraint problems.
4. **LLM Judge cost** — sample 10-20%, cache results, use smaller models for bulk scoring.

---

## ✅ Status: Done
