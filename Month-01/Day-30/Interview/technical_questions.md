# 🎯 Day 30 Technical Interview Questions: GenAI System Design

### Q1: How would you design a multi-tenant GenAI platform serving 10,000 requests/sec with strict cost controls?
**Architecture Framework**:
1. **API Ingress Layer**: Multi-region Envoy proxies with distributed Redis token bucket rate limiting enforcing dual RPM and TPM limits per tenant API key.
2. **Semantic Cache Cluster**: Redis cluster caching high-frequency queries with vector similarity, achieving ~35% cache hit rate and eliminating downstream GPU costs.
3. **Model Routing Tier**: Dynamic classifier analyzing query intent, directing 75% of queries to quantized open-source models (vLLM on L40S GPUs) and 25% to frontier reasoning APIs (Claude 3.5 Sonnet / GPT-4o).
4. **Resilience & Fallback**: Asynchronous task queues (Kafka + Celery) for non-interactive requests, with automated provider failover upon 429 rate limit errors.
5. **Observability**: OpenTelemetry spans logging token accounting, dollar cost per tenant, and $p95$ latency into Prometheus and Grafana dashboards.

---

### Q2: What is PagedAttention and why does it revolutionize LLM inference throughput?
**Answer**:
Traditional LLM inference pre-allocates contiguous virtual memory for the KV-cache of every request up to `max_tokens`. Because actual sequence lengths are dynamic, 60% to 80% of GPU memory was wasted due to internal and external memory fragmentation.
- **PagedAttention (vLLM)**: Inspired by virtual memory and paging in OS kernels. It partitions the KV-cache into non-contiguous fixed-size memory blocks (pages).
- By allowing key and value vectors to reside in non-contiguous physical GPU memory, it eliminates fragmentation, enabling up to 4x higher batch sizes and throughput on the same GPU hardware.
