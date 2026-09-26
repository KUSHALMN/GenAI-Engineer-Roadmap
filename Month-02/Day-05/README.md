# 📅 Day 35 — Month 02, Day 05: LLM Evaluation & Testing

> Build a golden evaluation dataset, rule-based evaluator, RAG triad evaluator, and pairwise LLM-as-a-judge system with position-bias mitigation. Implement Two Pointers DSA patterns in Python and Java.

---

## 📁 Structure

```
Day-05/
├── eval_dataset.jsonl      # Golden evaluation benchmark dataset
├── rule_based_eval.py      # Exact match, token F1, keyword coverage metrics
├── rag_eval.py             # Context relevance, faithfulness, and answer relevance
├── llm_judge.py            # Pairwise LLM-as-a-judge with order-swapping debiasing
├── evaluation_report.md    # Analysis of evaluation runs & hallucination metrics
├── two_pointers.py         # Two Pointers pattern in Python (LC 167, 15, 11, 125)
├── README.md
└── DSA/
    └── TwoPointers.java    # Two Pointers in Java (LC 167, LC 15, LC 11)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python rule_based_eval.py
python rag_eval.py
python llm_judge.py
python two_pointers.py
```

### Java Tests
```bash
cd DSA
javac TwoPointers.java
java TwoPointers
```

---

## ✅ Status: Completed
