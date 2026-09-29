# 📅 Day 22 — Month 02: Advanced RAG Triad Evaluator + Sliding Window DSA

> Build an enterprise RAG Triad evaluation microservice measuring Context Relevance, Faithfulness, and Answer Relevance with fine-grained hallucination detection. Master Sliding Window patterns (LC 3, 209, 438) in Java.

---

## 📁 Product Architecture

```
Day-22/
├── AI/
│   └── rag-triad-evaluator/
│       ├── app/
│       │   ├── api.py                   # FastAPI service (/health, /api/v1/evaluate/rag)
│       │   ├── config.py                # Quality thresholds and settings
│       │   └── runner.py                # Batch dataset evaluator
│       ├── core/
│       │   ├── triad_metrics.py         # Context Relevance, Faithfulness, Answer Relevance
│       │   ├── hallucination_detector.py# Fine-grained sentence & entity grounding
│       │   └── llm_judge.py             # Groq LLM Triad Judge with offline fallback
│       ├── data/
│       │   └── eval_dataset.json        # Golden RAG Q&A benchmark datasets
│       ├── tests/
│       │   └── test_rag_triad.py        # Pytest test suite
│       ├── Dockerfile                   # Container definition
│       ├── requirements.txt             # Service dependencies
│       └── README.md
├── DSA/
│   └── SlidingWindow.java               # LC 3 + LC 209 + LC 438 (Java)
├── Interview/
│   └── technical_questions.md           # RAG Triad, EM vs F1, Sliding Window types
├── Notes/
│   └── notes.md                         # Deep-dive study notes
└── README.md
```

---

## 🧠 AI: RAG Triad Microservice

### 1. Run Unit Tests
```bash
python -m pytest Month-02/Day-22/AI/rag-triad-evaluator/tests/test_rag_triad.py -v
```

### 2. Run Pipeline
```bash
python Month-02/Day-22/AI/rag-triad-evaluator/app/runner.py
```

### 3. Start FastAPI Service
```bash
uvicorn app.api:app --app-dir Month-02/Day-22/AI/rag-triad-evaluator --port 8000
```

---

## ☕ DSA: Sliding Window (Java)

```bash
cd Month-02/Day-22/DSA
javac SlidingWindow.java && java SlidingWindow
```

---

## ✅ Status: Production Complete
