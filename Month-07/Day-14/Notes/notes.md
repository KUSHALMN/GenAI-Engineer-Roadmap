# 📝 Notes — Day 14: CD Release Strategies & Memory Profiling

## 1. Canary Guardrail Metrics
- **HTTP 5xx Error Rate:** Trip rollback if error rate > 1%.
- **P99 Inference Latency:** Rollback if latency increases by > 20%.
- **Hallucination / Quality Score:** Automated evaluation on sampled responses.
