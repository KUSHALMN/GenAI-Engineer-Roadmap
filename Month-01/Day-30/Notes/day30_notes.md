# 📝 Day 30 Study Notes: GenAI System Design & Architecture Patterns

## 1. High-Scale GenAI Architecture Blueprint
When scaling a Generative AI platform to 10M+ daily active users, an end-to-end architecture consists of:
1. **Global CDN Edge / Anycast DNS**: TLS termination, DDoS filtering, geographic routing.
2. **GenAI API Gateway (Envoy / FastAPI / Kong)**:
   - Authentication & Tenant Quota Enforcement (Token Bucket for RPM and TPM).
   - Dynamic Model Router: Directs queries to cheap vs frontier models.
   - Semantic Caching layer (Redis vector store) answering hot queries in <15ms.
   - Pre-Execution Guardrails (toxicity, PII redaction, prompt injection defense).
3. **Async Task Worker Pools (Celery / Temporal / Kafka)**:
   - Handles long-running batch document embedding, video generation, and offline evals.
4. **Inference Serving Fleet (vLLM / Triton / TensorRT-LLM on AWS EKS with autoscaling GPUs)**:
   - Continuous batching (PagedAttention), KV-cache offloading, speculative decoding.

## 2. Token Bucket Rate Limiting (Dual RPM & TPM)
Traditional web APIs only limit requests/sec. In GenAI:
- One request might contain 50 tokens; another might contain 30,000 tokens (which exhausts model provider limits).
- The gateway must decrement both:
  - $\text{request\_tokens} \leftarrow \text{request\_tokens} - 1$
  - $\text{token\_budget} \leftarrow \text{token\_budget} - \text{estimated\_prompt\_tokens}$

## 3. Dynamic Model Routing Strategies
- **Cost Arbitrage**: 80% of customer questions are straightforward factual queries (e.g. "Store hours?", "Reset password?"). Routing these to lightweight models (\$0.15/1M) instead of frontier models (\$5.00/1M) slashes monthly cloud inference bills by over 85%.
- **Cascading Escalation**: Try fast model first with confidence check; escalate to frontier model only if confidence $< 0.80$.
