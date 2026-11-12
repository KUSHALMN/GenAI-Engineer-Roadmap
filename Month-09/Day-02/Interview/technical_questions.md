# 🎯 Technical Interview Questions — Day 02: Pretraining DataLoaders & Bellman-Ford

## Question 1: How do modern pretraining pipelines (e.g. Megatron-LM, Megatron-DeepSpeed) stream 10+ Terabytes of tokenized data without running out of RAM or bottlenecking GPU compute?
**Answer:**
1. **Memory-Mapped Binary Indices (`.bin` and `.idx`):** Token IDs are stored as packed contiguous 16-bit unsigned integers. A companion `.idx` file stores document boundary offsets. The OS kernel's virtual memory subsystem (`mmap`) reads disk blocks directly into the page cache on demand, consuming near-zero process memory.
2. **Deterministic Document Index Shuffling:** Instead of shuffling the multi-terabyte dataset itself, an array of document pointers is shuffled pseudo-randomly using a fixed seed, ensuring identical reproducible traversal across thousands of GPU workers.
3. **Double Buffering & CUDA Streams:** Background CPU worker threads prefetch the next micro-batch into pinned (page-locked) host memory (`cudaHostAlloc`) and transfer it asynchronously over PCIe via non-blocking CUDA streams while the GPU executes the forward/backward passes.

---

## Question 2: In LeetCode 787, why must Bellman-Ford create a copy of the distance array before each relaxation round?
**Answer:**
- Standard Bellman-Ford relaxes edges in-place across $V-1$ iterations.
- However, when the problem imposes a strict constraint of at most $K$ stops ($K+1$ edges), updating `dist` in-place allows an edge relaxed in the current round to immediately participate in relaxing another edge in the same iteration, chaining paths of length $> i+1$.
- Maintaining a frozen copy `temp = Arrays.copyOf(dist, n)` ensures each iteration strictly considers paths containing at most one additional hop, preserving the $K$-stop invariant.
