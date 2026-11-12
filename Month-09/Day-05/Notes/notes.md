# 📝 Notes — Day 05: Pipeline Parallelism & Kruskal's Algorithm

- **Pipeline Bubble Formula:** Bubble overhead fraction $F = \frac{P - 1}{P - 1 + M}$. Increasing micro-batches $M$ amortizes the bubble at the cost of longer step times.
- **Interleaved 1F1B:** Assigns multiple non-contiguous pipeline stages to each GPU (e.g. Stage 0 and Stage 4 on GPU 0), reducing the bubble fraction by a factor of $v$ (virtual stages).
- **Kruskal's Cycle Detection:** Two vertices $u, v$ belong to the same component if and only if `find(u) == find(v)`.
