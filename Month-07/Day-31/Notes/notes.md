# 📝 Notes — Day 31: Platform Benchmarking & Lock-Free Data Structures

## 1. High-Throughput Benchmarking Rules
- Always measure tail latency (P95, P99, P99.9) alongside mean latency.
- Warm up memory caches before measuring steady-state performance.
