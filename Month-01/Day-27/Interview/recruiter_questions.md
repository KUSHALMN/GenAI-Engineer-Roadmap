# 💼 Day 27 Recruiter & System Architecture Interview Questions

### 1. "How do you monitor and debug LLMs in production without violating user privacy?"
**Talking Points**:
- "We implement end-to-end distributed tracing using OpenTelemetry spans.
- To protect user privacy, we decouple operational telemetry (tokens consumed, TTFT, span duration, error rate, model identifier) from raw conversational payload text.
- PII is masked by our gateway before telemetry reaches logging collectors.
- We monitor latency percentiles ($p50, p95, p99$) and token burn rates in real time, alerting on anomalous cost spikes or degradation in TTFT."

### 2. "What are your strategies for controlling cloud inference costs?"
**Talking Points**:
- "We use three core levers:
  1. Real-time cost telemetry per endpoint and per tenant to establish clear accountability.
  2. Semantic caching to serve repeat queries instantly at zero model cost.
  3. Dynamic model routing: dispatching simple factual queries to fast, lightweight models ($0.15/1M tokens) while reserving frontier reasoning models ($5.00/1M tokens) for complex tasks."
