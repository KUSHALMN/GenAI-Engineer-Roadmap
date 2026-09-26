# 🏗️ Production RAG System Design Architecture

## 1. High-Level Architecture Diagram Flow

```
[ Client Applications ]
        │  HTTPS / WSS
        ▼
[ API Gateway / Reverse Proxy (Envoy / Kong) ]
        │  Auth, Rate Limiting, TLS Termination
        ▼
[ Security & Guardrails Layer ]
   ├── Input Sanitization & Jailbreak Filter
   └── PII Anonymizer
        │
        ▼
[ Semantic & Exact Cache Layer (Redis / Momento) ]
   ├── Exact SHA-256 Hit ───────────────┐
   └── Semantic Vector Hit (cos > 0.95) ─┤
        │ Miss                           │
        ▼                                │ Return Cached (<5ms)
[ Query Orchestration & Rewriting ]       │
   ├── HyDE (Hypothetical Embeddings)    │
   └── Sub-query Decomposition           │
        │                                │
   ┌────┴────────────────────────┐       │
   ▼                             ▼       │
[ Sparse BM25 Index ]   [ Dense Vector DB ]
(Elasticsearch / OpenSearch) (Pinecone / Qdrant / Milvus)
   └────┬────────────────────────┬┘
        ▼                        ▼
[ Reciprocal Rank Fusion (RRF) & Metadata Filter ]
        │ Top 50 Candidates
        ▼
[ Cross-Encoder Reranker (Cohere / BGE-Reranker) ]
        │ Top 5 Filtered & Ranked Chunks
        ▼
[ Model Gateway & Fallback Router (LiteLLM / Custom) ]
   ├── Primary: GPT-4o / Claude 3.5 Sonnet
   └── Fallback: LLaMA-3.1-70B (Groq / vLLM)
        │
        ▼
[ Output Guardrail & Inline Citation Attributor ]
   ├── Verify Groundedness & Provenance
   └── Redact Leaked Secrets
        │
        ├────────────────────────────────┘
        ▼
[ Client Response with Streamed Tokens ]
        │
        ▼
[ Async Observability & LLMOps (OTel + Prometheus + Arize Phoenix) ]
   ├── Latency Traces (TTFT, ITL)
   ├── Token Usage & Cost Attribution
   └── Golden Evaluation Sampling Queue
```

---

## 2. Ingestion Pipeline (Offline / Async)
- **Document Extractors**: PyMuPDF / Unstructured / OCR for images and PDFs.
- **Chunking Strategy**: Semantic hierarchy chunking ($512$ tokens with $64$ token overlap) preserving markdown headers.
- **Embedding Engine**: BGE-large-en-v1.5 / OpenAI text-embedding-3-small batched via Kafka/SQS queues.
- **Dual Indexing**:
  - Inverted term index in Elasticsearch/OpenSearch for exact part numbers, acronyms, and names.
  - HNSW index in Qdrant/Pinecone for semantic similarity.

---

## 3. Query Execution Pipeline (Online)
1. **Semantic Cache Lookup**: Compute SHA256 of normalized query; if miss, check cosine distance of query embedding against recent cache entries ($\tau \ge 0.95$).
2. **Hybrid Search**: Query both sparse and dense indexes in parallel; fuse via $RRF = \sum \frac{1}{60 + \text{rank}}$.
3. **Reranking**: Feed top 25 chunks through a cross-encoder to select top 3–5 chunks.
4. **LLM Generation**: Prompt with strict provenance constraints and numbered citation requirements.
