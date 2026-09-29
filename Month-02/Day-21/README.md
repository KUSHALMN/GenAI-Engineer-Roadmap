# 📅 Day 21 — Month 02: LLM Evaluation Framework + Two Pointers DSA

> Build a complete LLM evaluation framework with Exact Match, Token F1, and LLM-as-Judge metrics. Master Two Pointers patterns (LC 167, 15, 11) in Java.

---

## 📁 Structure

```
Day-21/
├── data/
│   └── eval_dataset.json       # 5 QA samples with context + expected answers
├── evaluation/
│   ├── exact_match.py          # EM + Normalized EM scoring
│   ├── keyword_match.py        # Token F1 + keyword overlap
│   ├── llm_judge.py            # LLM-as-Judge via Groq (correctness/faithfulness/helpfulness)
│   └── evaluator.py            # Main orchestrator — runs all metrics, saves report
├── results/
│   └── evaluation_report.json  # Output metrics report
├── DSA/
│   └── TwoPointers.java        # LC 167 + LC 15 + LC 11 (Java)
└── Interview/
    └── technical_questions.md  # RAG Triad, EM limits, position bias, Two Pointers vs Sliding Window
```

---

## 🧠 AI: LLM Evaluation

### Run Evaluator
```bash
cd Month-02/Day-21/evaluation
python evaluator.py
```

### Metrics Pipeline
| Metric | What it measures |
|--------|-----------------|
| Exact Match | Character-perfect match |
| Normalized EM | Case/punctuation-insensitive match |
| Token F1 | Keyword overlap precision/recall |
| LLM Judge | Correctness, faithfulness, helpfulness (1-5) |

---

## ☕ DSA: Two Pointers (Java)

```bash
cd Month-02/Day-21/DSA
javac TwoPointers.java && java TwoPointers
```

**Expected:**
```
[1, 2]
[[-1, -1, 2], [-1, 0, 1]]
49
```

---

## ✅ Status: Done
