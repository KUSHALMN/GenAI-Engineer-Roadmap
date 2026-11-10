# 🎯 Technical Interview Questions — Day 24: GPU Deployment & Code Review

### 1. When is self-hosting an open-source model (e.g. Llama-3-8B on dedicated GPUs) more economical than proprietary APIs?
**Answer:**
Breakeven analysis:
- At low or irregular traffic volumes (<5M tokens/day), managed pay-per-token APIs are vastly cheaper with zero maintenance overhead.
- When continuous throughput exceeds ~100 requests/second (millions of tokens per hour 24/7), a reserved instance (e.g., AWS EC2 `g5.2xlarge` @ $1.21/hr = ~$880/mo) becomes dramatically cheaper than pay-per-token APIs, offering lower P99 latencies and guaranteed data privacy.

### 2. What code smells do you prioritize identifying during pull request reviews?
**Answer:**
1. **Concurrency hazards:** Unsynchronized access to mutable state or unsafe publication.
2. **Resource Leaks:** Database connections, streams, or HTTP responses not closed via `try-with-resources`.
3. **N+1 Query Problems:** Database queries triggered inside loops rather than batch joins.
4. **Missing Timeout Boundaries:** Network calls without strict socket/connection timeouts.
