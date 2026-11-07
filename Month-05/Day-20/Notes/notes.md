# Day 20 Notes: Batching and Continuous Batching

## 1. Batching Comparison
- **Static:** High latency, waste due to padding.
- **Dynamic:** Groups similar lengths, but still blocks on longest.
- **Continuous (Orca / vLLM):** Per-iteration scheduling with zero bubble waste.
