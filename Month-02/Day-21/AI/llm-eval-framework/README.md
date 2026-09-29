# 📊 Enterprise LLM Evaluation Framework

Production microservice for evaluating generative AI systems. Combines deterministic lexical metrics (Exact Match, Token F1) with probabilistic LLM-as-a-Judge evaluations.

---

## 🏗️ Architecture

```
llm-eval-framework/
├── app/
│   ├── api.py            # FastAPI endpoints (/health, /evaluate/single, /evaluate/batch)
│   ├── config.py         # App configuration & score thresholds
│   └── runner.py         # Batch dataset evaluation runner
├── core/
│   ├── metrics.py        # Exact Match, Normalized EM, Token Precision/Recall/F1
│   └── llm_judge.py      # LLM-as-a-Judge scoring with Groq & mock fallbacks
├── data/
│   └── eval_dataset.json # Ground-truth benchmark datasets
├── tests/
│   └── test_evaluator.py # Pytest test suite
├── Dockerfile            # Container definition
├── requirements.txt      # Production dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Run Unit Tests
```bash
pytest tests/ -v
```

### 2. Run Local Evaluation Pipeline
```bash
python -m app.runner
```

### 3. Launch FastAPI Server
```bash
uvicorn app.api:app --reload --port 8000
```

### 4. Run via Docker
```bash
docker build -t llm-eval-framework .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key llm-eval-framework
```
