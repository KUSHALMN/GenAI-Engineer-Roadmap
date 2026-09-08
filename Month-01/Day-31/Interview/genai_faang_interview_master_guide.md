# 🏆 Day 31 Capstone Master Guide: Senior GenAI & FAANG Technical Interview Playbook

This master guide consolidates core technical concepts, architectures, and high-frequency interview questions across all 31 days of Month 01.

---

## 🏛️ PART 1: Core GenAI Architectural Pillars

### 1. The Production Latency Hierarchy
| Stage | Primary Bottleneck | Optimization Mechanism |
|---|---|---|
| **Network & Ingress** | TLS handshakes, slow reverse proxies | Edge termination, HTTP/2, keep-alive connections |
| **Prefill (TTFT)** | GPU KV-cache computation on long prompts | Prefix caching (vLLM/SGLang), prompt compression |
| **Generation (TPOT)** | Memory bandwidth-bound autoregressive decoding | PagedAttention, speculative decoding, continuous batching |
| **Client Perceived Latency** | Waiting for full text completion | Server-Sent Events (SSE) streaming tokens immediately |

---

### 2. High-Frequency Interview Questions (Top 10)

#### Q1: What is the difference between PagedAttention and standard multi-head attention?
**Answer**:
Standard attention requires contiguous virtual memory allocated for the KV-cache of every request up to its `max_tokens`, causing massive internal and external memory fragmentation (often 60-80% memory waste). PagedAttention partitions the KV cache into fixed-size virtual blocks (e.g. 16 tokens/block), allowing non-contiguous physical GPU allocation. This unlocks virtual memory sharing, parallel sampling, and 2-4x higher concurrent batch sizes.

#### Q2: How do you mathematically implement Reciprocal Rank Fusion (RRF)?
**Answer**:
For each document $d$ present across $K$ distinct retriever rankings (e.g., BM25 and Dense HNSW):
$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
where $r_m(d)$ is the 1-based rank position of $d$ in retriever $m$, and $k$ is a smoothing constant (typically 60). RRF eliminates score scale discrepancies (e.g. BM25 unbounded scores vs cosine [-1, 1] similarities) and rewards documents that perform consistently well across both modalities.

#### Q3: Why does Cross-Encoder reranking improve RAG answer quality?
**Answer**:
Bi-encoders compute vector embeddings of queries and documents independently ($f(q) \cdot f(d)$), losing deep token-to-token contextual relationships. Cross-encoders feed query and document jointly into transformer attention layers ($f(q, d)$), allowing all attention heads to evaluate cross-token semantic alignment, negation, and exact phrase matching.

#### Q4: How does a Semantic Cache differ from an exact Redis cache?
**Answer**:
An exact Redis cache hashes the exact string (`md5(prompt)`). A slight variation (e.g. *"What is RAG?"* vs *"Explain what RAG means"*) results in a cache miss. A Semantic Cache embeds queries into vector space and queries an in-memory cosine index. If similarity exceeds a threshold (e.g. 0.90), the cached answer is served in <10ms, slashing LLM token costs by 30-50%.

#### Q5: How do you design an LLM rate limiter for an enterprise platform?
**Answer**:
Traditional rate limiters only track Requests Per Minute (RPM). GenAI systems must enforce a dual Token Bucket algorithm:
1. RPM Token Bucket for request bursts.
2. TPM (Tokens Per Minute) Token Bucket tracking cumulative prompt + completion token usage. If either bucket empties, the request is throttled with HTTP 429.

#### Q6: What is Indirect Prompt Injection and how is it mitigated?
**Answer**:
Indirect prompt injection occurs when an LLM reads external untrusted content (e.g. websites, customer emails, uploaded PDFs) containing adversarial instructions disguised as text.
*Mitigations*:
1. Structural delimiter sandboxing (`<retrieved_context>` tags).
2. Input firewall scanning for prompt injection heuristics.
3. Strict tool permission scoping (read-only, requiring Human-In-The-Loop confirmation for sensitive writes).

#### Q7: How do you guarantee deterministic structured JSON outputs from LLMs?
**Answer**:
1. Grammar-based logit masking (e.g. Outlines, GBNF) at inference time.
2. Pydantic V2 schema validation with automated sanitization (stripping markdown fences, trailing commas).
3. The Instructor error-feedback loop: if validation fails, supply the validation error diff back to the model for self-healing.

#### Q8: What are the three primary failure modes diagnosed by RAGAS?
**Answer**:
1. Low Faithfulness: The answer makes claims not grounded in the retrieved text (hallucination).
2. Low Answer Relevance: The answer does not address the core query.
3. Low Context Recall: The retriever failed to locate relevant ground-truth snippets.

#### Q9: How do you handle LLM provider rate limits in a mission-critical pipeline?
**Answer**:
1. Exponential backoff with Full Jitter to avoid synchronized thundering-herd retry spikes.
2. Dynamic Multi-Model Fallback cascade: failover from primary frontier models to backup lightweight models.
3. Circuit breaker tripping to protect thread pools during extended outages.

#### Q10: How do you monitor LLM applications in production?
**Answer**:
Instrument all calls with OpenTelemetry spans tracking:
- Latency percentiles ($p50, p95, p99$) and TTFT.
- Token accounting (prompt, completion, total).
- Real-time financial cost per tenant.
- Anomaly alerts for sudden token burn or drop in completion length.
