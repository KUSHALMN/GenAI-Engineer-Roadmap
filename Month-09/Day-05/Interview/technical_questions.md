# 🎯 Technical Interview Questions — Day 05: Pipeline 1F1B & Kruskal's MST

## Question 1: Why does 1F1B (One-Forward-One-Backward) scheduling achieve significantly lower peak memory than GPipe while maintaining identical throughput?
**Answer:**
1. **GPipe Activation Accumulation:** In GPipe, all $M$ micro-batches execute their forward passes sequentially before the backward passes begin. Therefore, the first pipeline stage must stash activation tensors for all $M$ micro-batches simultaneously in GPU VRAM, leading to catastrophic out-of-memory (OOM) errors for large batch sizes.
2. **1F1B Steady-State Balance:** After an initial warmup of $P$ micro-batches, each worker runs one backward pass as soon as its downstream backward activation arrives, freeing that micro-batch's stashed activation *before* executing the next forward pass.
3. **Memory Bound:** Peak activation memory is strictly capped at $P$ micro-batches (the number of pipeline stages) rather than $M$, enabling pretraining with arbitrary numbers of micro-batches without increasing memory.

---

## Question 2: Compare Kruskal's and Prim's algorithms: when is Kruskal's preferred over Prim's, and how does Path Compression achieve near O(1) time?
**Answer:**
- **Sparse vs Dense Graphs:**
  - Kruskal's sorts all edges ($O(E \log E)$), making it ideal for sparse graphs where $E \ll V^2$.
  - Prim's with adjacency lists or matrices is more efficient on dense graphs ($E \approx V^2$).
- **Union-Find Invariants:**
  - **Path Compression:** Flattens the tree during `find(i)` by making every traversed node point directly to the root (`parent[i] = find(parent[i])`).
  - **Union by Rank:** Always attaches the shallower tree under the root of the deeper tree, preventing pathological linear degenerate chains.
  - Combined, any sequence of $M$ operations on $N$ elements takes $O(M \cdot \alpha(N))$ time, where $\alpha$ is the Inverse Ackermann function (effectively constant $\le 4$ for all practical input sizes).
