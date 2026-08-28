# 📄 Enterprise PDF RAG Chatbot with Streaming & Hybrid Retrieval

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot engineered with **FastAPI**, **Hybrid Search (BM25 + Dense Semantic Embeddings)**, **Reciprocal Rank Fusion (RRF)**, **Citation Tracking**, and **Server-Sent Events (SSE) Token Streaming**.

---

## 🚀 Key Features

- **Hybrid Retrieval Engine**:
  - **Dense Semantic Embeddings**: Captures semantic nuance and conceptual similarity.
  - **Sparse Okapi BM25**: Precise exact keyword, acronym, and technical code retrieval.
  - **Reciprocal Rank Fusion (RRF)**: Merges sparse and dense scores for optimal ranking.
- **Real-Time Token Streaming**:
  - Asynchronous Server-Sent Events (`/api/v1/query/stream`) for typewriter effect.
  - Returns Time-to-First-Token (TTFT) and total latency performance metrics.
- **Verifiable Citations**:
  - Returns exact document source filename, page number, chunk ID, and snippet for zero-hallucination auditing.
- **Enterprise Ready**:
  - Fully typed Pydantic validation schemas.
  - Multi-stage Dockerized container with non-root security.
  - Pytest unit and integration test suite.

---

## 🏗️ Architecture Flow

```
[ PDF / Text Ingestion ] ──> [ Page Extraction (pypdf) ] ──> [ Recursive Chunker ]
                                                                     │
                                    ┌────────────────────────────────┴────────────────────────────────┐
                                    ▼                                                                 ▼
                        [ Dense Vector Store ]                                             [ Okapi BM25 Index ]
                                    │                                                                 │
                                    └────────────────────────────────┬────────────────────────────────┘
                                                                     ▼
                                                    [ Reciprocal Rank Fusion (RRF) ]
                                                                     │
                                                                     ▼
                                                    [ Prompt Builder + Citations ]
                                                                     │
                                                                     ▼
                                                   [ SSE Streaming / REST API ]
```

---

## 📦 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Healthcheck and index diagnostics |
| `POST` | `/api/v1/upload` | Upload and index PDF documents (multipart/form-data) |
| `POST` | `/api/v1/ingest-text` | Ingest raw text directly for testing |
| `POST` | `/api/v1/query` | Synchronous RAG query with citations |
| `POST` | `/api/v1/query/stream` | Server-Sent Events (SSE) live streaming query |
| `GET` | `/api/v1/documents` | View indexed documents and statistics |
| `DELETE` | `/api/v1/documents` | Clear indexed database |

---

## 🛠️ Quickstart Guide

### 1. Run Locally
```bash
# Navigate to project directory
cd Month-01/Day-22/AI/pdf-rag-chatbot

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

### 2. Run with Docker
```bash
# Build Docker image
docker build -t pdf-rag-chatbot:latest .

# Run container
docker run -p 8000:8000 --env LLM_PROVIDER=mock pdf-rag-chatbot:latest
```

### 3. Run Test Suite
```bash
pytest tests/ -v
```

---

## 📡 Example Usage

### Ingest Text:
```bash
curl -X POST "http://localhost:8000/api/v1/ingest-text" \
     -H "Content-Type: application/json" \
     -d '{"title": "rag_overview.txt", "content": "RAG reduces hallucinations by grounding responses in verified vector embeddings and text chunks."}'
```

### Query with Citations:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "How does RAG reduce hallucinations?", "top_k": 3}'
```

### Stream Live Responses:
```bash
curl -N -X POST "http://localhost:8000/api/v1/query/stream" \
     -H "Content-Type: application/json" \
     -d '{"question": "Explain RAG architecture"}'
```
