# Notes: Production RAG API Engineering

## 1. REST Endpoint Specifications
- `POST /v1/ingest`: Accepts document metadata, text chunks, and access controls. Hashes chunks to enable idempotent upserts.
- `POST /v1/query`: Accepts user query, tenant identifier, and top-K. Returns answer, citation arrays, and latency metrics.
- `POST /v1/feedback`: Collects explicit user thumbs up / down signals, correlating them with `query_id` for offline RLHF or reranker fine-tuning.
- `GET /v1/health`: Kubernetes readiness and liveness probe verifying database connectivity, vector index availability, and GPU/model endpoints.

## 2. Error Envelopes & Input Validation
All endpoints enforce strict Pydantic schemas:
- Returning `422 Unprocessable Entity` for malformed payloads.
- Returning `400 Bad Request` for empty chunks or missing query text.
- Returning `429 Too Many Requests` when rate limits are exceeded.
