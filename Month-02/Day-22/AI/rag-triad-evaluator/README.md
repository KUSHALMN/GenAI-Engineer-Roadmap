# 🎯 Enterprise RAG Triad Evaluator & Hallucination Guardrail

Production evaluation service for measuring Retrieval-Augmented Generation (RAG) quality across Context Relevance, Faithfulness, and Answer Relevance, augmented with entity-level hallucination detection.

---

## 🏗️ Architecture

```
rag-triad-evaluator/
├── app/
│   ├── api.py                   # FastAPI service (/health, /api/v1/evaluate/rag)
│   ├── config.py                # Quality thresholds and settings
│   └── runner.py                # Batch dataset evaluator
├── core/
│   ├── triad_metrics.py         # Context Relevance, Faithfulness, Answer Relevance
│   ├── hallucination_detector.py# Fine-grained sentence & entity grounding
│   └── llm_judge.py             # Groq LLM Triad Judge with offline fallback
├── data/
│   └── eval_dataset.json        # Golden RAG Q&A benchmark datasets
├── tests/
│   └── test_rag_triad.py        # Pytest test suite
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

### 2. Run Pipeline
```bash
python -m app.runner
```

### 3. Launch API
```bash
uvicorn app.api:app --reload --port 8000
```
