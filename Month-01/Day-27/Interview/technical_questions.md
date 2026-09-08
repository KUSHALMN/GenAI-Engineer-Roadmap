# 🎯 Day 27 Technical Interview Questions: LLM Observability & Metrics

### Q1: Why is tracking average latency insufficient for GenAI systems?
**Answer**:
Average latency obscures catastrophic tail performance. In autoregressive LLMs, token generation is proportional to output length. A few 2,000-token queries (taking 25 seconds) will be smoothed over by thousands of 50-token queries (taking 700ms).
- **p95 and p99 percentiles** reveal the true worst-case experience of enterprise users.
- Analyzing the distribution between **TTFT** (prefill/retrieval bottleneck) and **TPOT** (model generation throughput) tells engineers whether to optimize vector database index parameters or batching schedulers.

---

### Q2: How do you implement real-time cost attribution across enterprise tenants?
**Answer**:
1. At the API Gateway, extract the authenticated tenant ID (`tenant_id`).
2. Attach `tenant_id` as an attribute on the parent OpenTelemetry trace.
3. In the LLM span wrapper, intercept the model response `usage` object (`prompt_tokens`, `completion_tokens`).
4. Apply the pricing matrix dynamically and push a Prometheus counter:
   `llm_cost_total{tenant="acme_corp", model="gpt-4o"}`.
5. Trigger automated billing threshold alerts if a tenant consumes >80% of their daily token quota.
