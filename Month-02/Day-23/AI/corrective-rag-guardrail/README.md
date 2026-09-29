# 🛡️ Enterprise Corrective RAG (CRAG) & Self-RAG Guardrails

Production microservice implementing Corrective Retrieval-Augmented Generation (CRAG) and Self-RAG reflection tokens to guarantee groundedness, prevent hallucinations, and dynamically self-heal retrieval failures.

---

## 🏗️ Architecture

```
corrective-rag-guardrail/
├── app/
│   ├── api.py                   # FastAPI service (/health, /api/v1/crag/query, /api/v1/self-rag/reflect)
│   ├── config.py                # Threshold configs
│   └── crag_engine.py           # Retrieval, evaluation, and striping orchestrator
├── core/
│   ├── retrieval_evaluator.py   # Document grading (CORRECT, AMBIGUOUS, INCORRECT)
│   ├── knowledge_refiner.py     # Sentence-level striping and noise elimination
│   ├── query_transformer.py     # Query rewriter and web fallback
│   └── self_rag_guardrail.py    # [Retrieve], [IsRel], [IsSup], [IsUse] critique tokens & auto-repair
├── data/
│   └── knowledge_base.json      # Gold knowledge store
├── tests/
│   └── test_crag.py             # Pytest test suite
├── Dockerfile                   # Container definition
├── requirements.txt             # Service dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Run Unit Tests
```bash
python -m pytest tests/ -v
```

### 2. Run Direct Query
```bash
python -m app.crag_engine
```

### 3. Launch API
```bash
uvicorn app.api:app --reload --port 8000
```
