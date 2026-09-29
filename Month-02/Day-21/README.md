# 📅 Day 21 — Month 02: Enterprise LLM Evaluation Service + Two Pointers DSA

> Build a production-grade LLM evaluation microservice featuring Lexical Metrics (Exact Match, Normalized EM, Token F1), Groq LLM-as-a-Judge, and a FastAPI service. Master Two Pointers patterns (LC 167, 15, 11) in Java.

---

## 📁 Product Architecture

```
Day-21/
├── AI/
│   └── llm-eval-framework/
│       ├── app/
│       │   ├── api.py                 # FastAPI microservice (/health, /evaluate/*)
│       │   ├── config.py              # Settings & threshold configs
│       │   └── runner.py              # Batch evaluation pipeline runner
│       ├── core/
│       │   ├── metrics.py             # Exact Match, Normalized EM, Token F1
│       │   └── llm_judge.py           # Groq LLM-as-a-Judge with offline fallback
│       ├── data/
│       │   └── eval_dataset.json      # Gold reference benchmark dataset
│       ├── tests/
│       │   └── test_evaluator.py      # Pytest validation test suite
│       ├── Dockerfile                 # Production Docker image
│       ├── requirements.txt           # App dependencies
│       └── README.md                  # Microservice documentation
├── DSA/
│   └── TwoPointers.java               # LC 167 + LC 15 + LC 11 (Java)
├── Interview/
│   └── technical_questions.md         # RAG Triad, EM limits, position bias
├── Notes/
│   └── notes.md                       # Deep-dive study notes
└── README.md
```

---

## 🧠 AI: LLM Evaluation Microservice

### 1. Run Unit Tests
```bash
python -m pytest Month-02/Day-21/AI/llm-eval-framework/tests/test_evaluator.py -v
```

### 2. Run Pipeline
```bash
python Month-02/Day-21/AI/llm-eval-framework/app/runner.py
```

### 3. Start FastAPI Service
```bash
uvicorn app.api:app --app-dir Month-02/Day-21/AI/llm-eval-framework --port 8000
```

---

## ☕ DSA: Two Pointers (Java)

```bash
cd Month-02/Day-21/DSA
javac TwoPointers.java && java TwoPointers
```

---

## ✅ Status: Production Complete
