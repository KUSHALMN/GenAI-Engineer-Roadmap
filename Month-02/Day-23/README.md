# 📅 Day 23 — Month 02: Corrective RAG (CRAG), Self-RAG & LRU Cache DSA

> Build an enterprise Corrective RAG (CRAG) microservice with dynamic retrieval evaluation, knowledge striping, and Self-RAG critique guardrails. Master LeetCode 146 (LRU Cache) in Java.

---

## 📁 Product Architecture

```
Day-23/
├── AI/
│   └── corrective-rag-guardrail/
│       ├── app/
│       │   ├── api.py                   # FastAPI service (/health, /api/v1/crag/query, /api/v1/self-rag/reflect)
│       │   ├── config.py                # Confidence and support thresholds
│       │   └── crag_engine.py           # Retrieval, evaluation, and striping orchestrator
│       ├── core/
│       │   ├── retrieval_evaluator.py   # Document grading (CORRECT, AMBIGUOUS, INCORRECT)
│       │   ├── knowledge_refiner.py     # Sentence-level striping & noise elimination
│       │   ├── query_transformer.py     # Query rewriter & web search fallback
│       │   └── self_rag_guardrail.py    # [Retrieve], [IsRel], [IsSup], [IsUse] critique tokens
│       ├── data/
│       │   └── knowledge_base.json      # Gold knowledge store
│       ├── tests/
│       │   └── test_crag.py             # Pytest test suite
│       ├── Dockerfile                   # Production container definition
│       ├── requirements.txt             # Service dependencies
│       └── README.md
├── DSA/
│   └── LRUCachePatterns.java            # LeetCode 146 LRU Cache (Java)
├── Interview/
│   └── technical_questions.md           # CRAG, Self-RAG tokens, LRU Cache O(1)
├── Notes/
│   └── notes.md                         # Deep-dive study notes
└── README.md
```

---

## 🧠 AI: CRAG & Self-RAG Microservice

### 1. Run Unit Tests
```bash
python -m pytest Month-02/Day-23/AI/corrective-rag-guardrail/tests/test_crag.py -v
```

### 2. Run Direct CLI Query
```bash
python Month-02/Day-23/AI/corrective-rag-guardrail/app/crag_engine.py
```

### 3. Start FastAPI Service
```bash
uvicorn app.api:app --app-dir Month-02/Day-23/AI/corrective-rag-guardrail --port 8000
```

---

## ☕ DSA: LRU Cache (Java)

```bash
cd Month-02/Day-23/DSA
javac LRUCachePatterns.java && java LRUCachePatterns
```

---

## ✅ Status: Production Complete
