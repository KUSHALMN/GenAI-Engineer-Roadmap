# 💥 Production GenAI Failure Modes & Mitigation Runbook

## 1. Upstream Model Provider Outage (HTTP 500 / 503)
- **Root Cause**: Azure/OpenAI/Anthropic regional downtime or model server crash.
- **Detection**: Spike in 5xx HTTP response codes from model gateway via Prometheus metrics.
- **Automated Mitigation**:
  - Model Gateway circuit breaker trips after 5 consecutive failures.
  - Automatically redirects traffic to standby secondary provider (e.g. Anthropic $\rightarrow$ Groq / AWS Bedrock).
  - Emits PagerDuty alert to on-call engineer.

---

## 2. Upstream Rate Limiting (HTTP 429)
- **Root Cause**: Sudden burst traffic exceeding contracted TPM (Tokens Per Minute) or RPM limits.
- **Detection**: Influx of 429 responses; local Token Bucket exhaustion.
- **Automated Mitigation**:
  - Request queuing with exponential backoff and full jitter.
  - Cache aggressive fallback: widen semantic cache cosine threshold to $0.90$.
  - Load-shedding non-critical background batch jobs.

---

## 3. Context Window Overflow & Token Exhaustion
- **Root Cause**: Accumulation of lengthy retrieved documents combined with long user chat histories.
- **Detection**: Provider returns invalid request error: `context_length_exceeded`.
- **Automated Mitigation**:
  - Dynamic token budget allocation in `ContextManager`.
  - Automatic dialogue summarization compressing older turns.
  - Truncation of low-scoring reranked documents prior to prompt assembly.

---

## 4. Vector Database Drift & Stale Retrieval
- **Root Cause**: Ingestion lag; outdated document chunks remaining in vector index after underlying data is updated.
- **Detection**: RAG evaluation pipeline flags drop in groundedness / faithfulness scores below $95\%$.
- **Automated Mitigation**:
  - Document versioning & TTL in metadata index.
  - Asynchronous tombstoning on document deletion webhook.
