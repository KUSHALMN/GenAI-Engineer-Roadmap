# 📅 Day 24: 🧠 Production Prompt Engineering & Word Break DSA

Welcome to **Day 24** of the **GenAI Engineer Roadmap**! Today focuses on building production-grade prompt templates, few-shot demonstration engines, Chain-of-Thought (CoT) structures, automated quantitative prompt evaluations (BLEU, ROUGE-L, Cosine Similarity), and mastering LeetCode 139 (Word Break) in Java.

---

## 📁 Day 24 Project Structure

```
Day-24/
├── AI/
│   └── prompt-engineering/
│       ├── src/
│       │   ├── templates.py        # Variable interpolation & Few-Shot builders
│       │   ├── evaluator.py        # BLEU, ROUGE-L, Cosine similarity & exact match
│       │   └── app.py              # CLI evaluation & benchmark report generator
│       ├── tests/
│       │   └── test_evaluator.py   # Automated metric test harness
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── templates.py
│   ├── evaluator.py
│   └── app.py
├── tests/
│   └── test_evaluator.py
│
├── DSA/
│   └── word_break.java             # LeetCode 139: Word Break (Optimized DP & Trie)
│
├── Interview/
│   ├── technical_questions.md       # Regression prevention, LLM-as-a-judge biases
│   ├── coding_questions.md          # Word Break DP recurrence & Trie optimization
│   └── recruiter_questions.md       # Quantitative prompt engineering talking points
│
├── Notes/
│   └── day24_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Production Prompt Templating**: Safe variable substitution and dynamic few-shot injection.
2. **Chain-of-Thought (CoT)**: Eliciting structured reasoning steps prior to final outputs.
3. **Deterministic & Semantic Evals**: Quantifying prompt changes using Exact Match, BLEU-1, ROUGE-L, and vector cosine similarity.
4. **Dynamic Programming / Trie DSA**: Optimal string segmentation via bounded memoization.

---

## 🚀 Execution Commands

### Test Prompt Evaluation Suite
```bash
python -m pytest Month-01/Day-24/tests/test_evaluator.py -v
```

### Run Word Break Java Solution
```bash
javac Month-01/Day-24/DSA/word_break.java
java -cp Month-01/Day-24/DSA word_break
```
