# 💼 Day 29 Recruiter & System Architecture Interview Questions

### 1. "How do you optimize an enterprise RAG system that is suffering from slow retrieval and hallucinations?"
**Talking Points**:
- "First, I diagnose the pipeline using RAGAS metrics to isolate whether the failure is in retrieval (low context recall) or generation (low faithfulness).
- To eliminate hallucinations caused by lost-in-the-middle context stuffing, I introduce a two-stage retrieval architecture:
  1. First stage: Hybrid dense/BM25 retrieval fetching 40 candidates.
  2. Second stage: Cross-Encoder reranker narrowing candidates to the 3 highest-scoring snippets.
- To reduce latency and inference cost, I place a semantic cache in front of the pipeline with a 0.88 cosine similarity threshold, serving common questions instantly."

### 2. "How do you handle real-time updates and deletions in vector databases?"
**Talking Points**:
- Vector databases like Qdrant and Pinecone maintain mutable point IDs with upsert semantics.
- When source documents change in Postgres or S3, a Change Data Capture (CDC) pipeline via Kafka/Debezium pushes update events to an asynchronous embedding worker.
- Document chunks carry a parent document UUID in metadata, allowing complete invalidation of outdated chunk vectors and clearing stale semantic cache entries."
