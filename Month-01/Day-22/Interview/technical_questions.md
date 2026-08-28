# 🎯 Day 22 - Technical Interview Preparation: RAG Systems, Streaming & Retrieval

---

### Q1: Explain the mathematical rationale behind Reciprocal Rank Fusion (RRF) in Hybrid Search.
**Answer:**
Reciprocal Rank Fusion (RRF) is an unsupervised score aggregation algorithm that combines rankings from multiple distinct retrieval mechanisms (e.g., Sparse Lexical BM25 and Dense Semantic Vector Search) without requiring score normalization.

#### Formula:
$$\text{RRF\_Score}(d \in D) = \sum_{m \in M} \frac{w_m}{k + r_m(d)}$$
where:
- $M$ is the set of retrieval models (e.g., BM25, Dense Vector).
- $w_m$ is the assigned weight for model $m$.
- $r_m(d)$ is the 1-based rank position of document $d$ in the result list of model $m$.
- $k$ is a smoothing constant (standard default is $k = 60$) that prevents top-ranked items from disproportionately dominating the score.

#### Why RRF over Score Averaging?
1. **Scale Invariance**: Dense cosine similarities lie in $[-1, 1]$ or $[0, 1]$, whereas BM25 scores are unbounded $[0, \infty)$. Raw score averaging requires complex min-max calibration, which varies per query. RRF only depends on relative rank order.
2. **Outlier Robustness**: If one retriever produces an anomalous high score for an irrelevant document, RRF dampens its impact because rank position $1$ contributes at most $1/(60+1) \approx 0.0163$.

---

### Q2: How does Server-Sent Events (SSE) differ from WebSockets for LLM Token Streaming?
**Answer:**

| Dimension | Server-Sent Events (SSE) | WebSockets |
|---|---|---|
| **Protocol** | Standard HTTP/1.1 or HTTP/2 | Bidirectional TCP upgrade (`ws://`, `wss://`) |
| **Directionality** | Unidirectional (Server $\to$ Client) | Full Duplex Bidirectional |
| **Payload Format** | UTF-8 Text (`text/event-stream`) | Binary or Text frames |
| **Connection Overhead** | Minimal (Standard HTTP keep-alive) | Protocol handshake & state management |
| **Firewall / Proxy** | Native support via standard HTTP ports | Sometimes blocked by enterprise proxies |
| **Automatic Reconnection**| Built-in browser event listener retry | Requires custom client-side reconnect logic |

**Best Practice for LLMs**: Since generative LLM token streaming is purely unidirectional (the prompt is sent once, and tokens stream back until completion), SSE is simpler, lighter, firewall-friendly, and leverages HTTP/2 multiplexing.

---

### Q3: What is Time to First Token (TTFT) and how do you optimize it in RAG architectures?
**Answer:**
**Time to First Token (TTFT)** measures the latency between when the user submits a query and when the first generated token appears on the client interface.

#### Optimization Strategies:
1. **Parallelized Retrieval**: Execute dense embedding vector search and BM25 keyword search concurrently using `asyncio.gather()`.
2. **Streaming Embeddings & Query Decomposition**: Cache frequent query embeddings in Redis.
3. **KV Cache & Prompt Caching**: Store pre-computed key-value states for static system prompts and document context.
4. **Fast Reranker Pipelines**: Use lightweight cross-encoders (e.g. FlashRank, MiniLM) capped at Top-10 candidates rather than full-sized models.

---

### Q4: How do you prevent hallucinations in PDF Q&A systems when documents contain conflicting or incomplete data?
**Answer:**
1. **Strict System Prompt Constraints**: Explicitly instruct the model: *"Answer strictly using only the provided context. If the answer is not present, reply 'I cannot find this information in the document.' Do not extrapolate."*
2. **Citation Grounding**: Require the model to tag every assertion with exact chunk indices `[Source: filename, Page: N]`.
3. **Confidence Thresholding**: If the top retrieved chunk similarity score is below a strict threshold (e.g., cosine similarity $< 0.35$), bypass the LLM and return a deterministic fallback message.
4. **Self-Correction / Verification Loop**: Run a lightweight secondary critique pass (e.g. RAG Triad: Context Relevance, Groundedness, Answer Relevance).
