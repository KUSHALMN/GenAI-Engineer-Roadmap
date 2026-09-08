# 📝 Day 27 Study Notes: LLM Observability, Tracing & Cost Telemetry

## 1. Why GenAI Needs Specialized Observability
Traditional APM (Datadog, New Relic) monitors CPU, memory, and HTTP status codes. However, GenAI applications present non-traditional failure modes:
1. **High Latency Variance**: A 50-token answer takes 800ms, while a 1,500-token answer takes 18 seconds. Mean latency is misleading; $p95$ and $p99$ tail latencies are essential.
2. **Financial Cost Risk**: A rogue user loop or bloated prompt can burn hundreds of dollars in minutes without throwing an HTTP error.
3. **Semantic Drift & Quality Degradation**: An API can return HTTP 200 OK while hallucinating or repeating repetitive loops.

## 2. Key Observability Metrics (The GenAI Golden Signals)
- **Token Accounting**:
  - `prompt_tokens`: Measures context size and vector retrieval efficiency.
  - `completion_tokens`: Measures model verbosity.
  - `total_tokens`: Determines billing and GPU compute saturation.
- **Latency Distribution**:
  - **TTFT (Time To First Token)**: Prefill phase speed.
  - **TPOT (Time Per Output Token)**: Generation throughput ($1 / \text{TPS}$).
  - **Total Span Duration**: End-to-end user request cycle.
- **Unit Economics**:
  - Estimated cost per transaction ($USD / 1k \text{ tokens}$).
  - Cost per tenant or user session.

## 3. OpenTelemetry Integration Architecture
- Use **Context Propagation** (`trace_id`, `parent_span_id`) to track requests across the API Gateway, Embedding service, Vector DB retrieval, Reranker, and LLM inference engine.
- Export telemetry spans via OTLP (OpenTelemetry Protocol) to backends like LangSmith, Arize Phoenix, OpenLLMetry, or Prometheus + Grafana.
