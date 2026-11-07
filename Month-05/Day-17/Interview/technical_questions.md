# Day 17: Technical Interview Preparation — Prefill vs Decode & Concurrency

### Q1: Why is LLM generation memory bandwidth-bound during decoding, while prefill is compute-bound?
**Answer:**
- **Prefill Phase:** The entire prompt is known upfront. The GPU can perform large matrix-matrix multiplications ($GEMM$), saturating Tensor Cores.
- **Decode Phase:** Tokens are produced sequentially one at a time. For every single generated token, the GPU must fetch all weights ($W$) from VRAM to SRAM ($GEMV$), consuming vast memory bandwidth while achieving low arithmetic intensity.

### Q2: Why is `ConcurrentHashMap` significantly faster than `Hashtable` or `Collections.synchronizedMap`?
**Answer:**
`Hashtable` synchronizes on the entire map instance, forcing all threads to queue up behind a single global lock. `ConcurrentHashMap` uses bucket-level synchronization (locking individual nodes) and lock-free volatile reads, allowing high concurrent throughput without blocking uncontended buckets.
