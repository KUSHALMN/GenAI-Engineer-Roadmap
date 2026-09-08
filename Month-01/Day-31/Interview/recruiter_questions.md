# 💼 Day 31 Recruiter & System Architecture Interview Questions: Month 01 Capstone

### 1. "Can you give me an executive overview of your Capstone GenAI Project?"
**Talking Points**:
- "For my Month 01 Capstone, I architected and built the **Enterprise Autonomous Support Copilot**, an end-to-end full-stack GenAI system built for high-throughput, enterprise-grade deployments.
- The platform unifies the eight core pillars of production GenAI:
  1. Real-time token streaming with Server-Sent Events (SSE) to eliminate user-perceived latency.
  2. Multi-tenant Token Bucket rate limiting enforcing strict dual RPM and TPM quotas.
  3. Pre-execution security firewalls blocking direct/indirect prompt injection with canary token tripwires.
  4. Optimized two-stage RAG with Cross-Encoder reranking and verifiable citations.
  5. High-hit-rate in-memory semantic caching delivering sub-15ms responses for recurring intents.
  6. Structured Pydantic V2 output validation with self-healing feedback loops.
  7. Automated fallback cascades with exponential backoff and full jitter.
  8. Full OpenTelemetry-compatible span tracing, cost accounting, and latency percentiles ($p50, p95, p99$)."

### 2. "What was the most challenging technical hurdle you solved during Month 01?"
**Talking Points**:
- "The biggest engineering challenge was balancing retrieval latency with answer precision.
- Initially, standard dense vector search retrieved irrelevant context that confused the LLM (the lost-in-the-middle problem).
- I solved this by implementing a two-stage hybrid retrieval pipeline: broad BM25 + dense vector recall fetching 40 candidate chunks, followed by a Cross-Encoder reranker narrowing down to the top 2-3 most relevant snippets.
- To neutralize the slight latency added by reranking, I placed an in-memory semantic cache in front of the pipeline, which served 35% of repeat queries in under 12ms at zero LLM cost."
