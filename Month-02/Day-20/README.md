# 📅 Day 50 — Month 02, Day 20: FAANG GenAI Interview & Production Capstone

> Complete production-grade GenAI Capstone Service: FastAPI backend, RAG & agent workflows, structured outputs, exact and TTL response caching, prompt injection security guardrails, PII masking, token cost attribution, Docker containerization, evaluation dataset, and comprehensive interview answers with DSA mock results.

---

## 📁 Structure

```
Day-20/
├── main.py                     # FastAPI application entrypoint with Auth & CORS
├── agent_service.py            # Core Capstone Agent service coordinating RAG, Tools & Caching
├── schemas.py                  # Pydantic data contracts (QueryRequest, QueryResponse)
├── security_guardrails.py      # Prompt injection defenses & PII masking
├── eval_dataset.jsonl          # Benchmark golden evaluation dataset
├── evaluate_capstone.py        # Automated end-to-end evaluation & speedup benchmark
├── Dockerfile                  # Security-hardened multi-stage non-root containerfile
├── docker-compose.yml          # Production stack deployment definition
├── requirements.txt            # Python dependencies
├── genai_interview_answers.md  # FAANG GenAI interview Q&A (RAG, vLLM, Security, TTFT)
├── dsa_mock_results.md         # Comprehensive scorecard across all 17 DSA patterns
├── behavioral_stories.md       # Senior GenAI Engineer STAR behavioral interview stories
├── final_self_assessment.md    # Month 2 Days 04-20 readiness assessment
├── README.md
└── DSA/
    └── CapstoneDSA.java        # Java DSA Masterclass (LRU, Top-K, Trie, Graph Cycle)
```

---

## 🚀 Running the Capstone

### 1. Run Automated Evaluation
```bash
python evaluate_capstone.py
```

### 2. Run FastAPI Server Locally
```bash
uvicorn main:app --reload --port 8000
```
- Open Swagger Docs: `http://localhost:8000/docs`
- Health check: `GET http://localhost:8000/health`
- Query endpoint: `POST http://localhost:8000/api/query` (Header: `X-API-Key: test-api-key`)

### 3. Run Java DSA Masterclass
```bash
cd DSA
javac CapstoneDSA.java
java CapstoneDSA
```

### 4. Deploy via Docker
```bash
docker-compose up --build -d
```

---

## ✅ Status: Month 2 Days 04 – 20 Complete!
