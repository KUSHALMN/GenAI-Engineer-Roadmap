# 📝 Day 29 Study Notes: Production RAG Optimization, Reranking & Semantic Caching

## 1. Why Standard RAG Fails in Production
A naive RAG pipeline (embed query -> top-k cosine search in vector DB -> send to LLM) suffers from:
1. **Low Precision (Bi-encoder Bottleneck)**: Dense embeddings compress an entire 500-token chunk into a single 1536-dimensional vector, losing fine-grained keyword relationships and numerical entities.
2. **Context Stuffing / Lost-in-the-Middle**: Feeding 10-20 raw chunks causes the model to ignore critical information placed in the middle of long prompts.
3. **High Latency & Costs**: Repetitive queries (e.g. *"What is the refund policy?"*) burn GPU cycles and LLM API fees repeatedly.

## 2. The Two-Stage Retrieval Architecture
Production systems decouple **Retrieval** from **Precision Ranking**:
- **Stage 1: High-Recall Retrieval (Broad Net)**:
  - Hybrid Search: Fuses sparse BM25 (exact keyword match) and dense HNSW vectors (semantic concept match) using Reciprocal Rank Fusion (RRF).
  - Fetches top 25 to 50 candidate chunks in < 25ms.
- **Stage 2: High-Precision Cross-Encoder Reranking**:
  - A Cross-Encoder feeds `[CLS] query [SEP] chunk [EOS]` together into transformer attention layers.
  - Allows full cross-attention between every query word and every document word.
  - Selects the top 3-5 most pertinent chunks with high precision.

## 3. Semantic Caching Architecture
- Store prior user queries alongside their embedding vectors in an in-memory or Redis index.
- For an incoming query $q_{new}$, compute cosine similarity against stored queries:
  $$\text{sim}(q_{new}, q_i) \ge \tau \quad (\tau \approx 0.88 - 0.92)$$
- If matched, serve the response in < 10ms at \$0 cost, bypassing both vector retrieval and LLM generation.
