# 🎯 Technical Interview Questions — Day 03: DDP Ring All-Reduce & Floyd-Warshall

## Question 1: Prove why the total data transmitted by each GPU in Ring All-Reduce is 2 * ((N - 1) / N) * S bytes, and why this is bandwidth-optimal.
**Answer:**
1. **Tensor Slicing:** A tensor of size $S$ is partitioned into $N$ equal chunks of size $S / N$.
2. **Scatter-Reduce Phase:** In each of the $N - 1$ steps, each rank sends one chunk of size $S / N$ to its clockwise neighbor and receives one chunk from its counter-clockwise neighbor, accumulating values. Total data sent = $(N - 1) \times (S / N)$.
3. **All-Gather Phase:** In each of the $N - 1$ steps, each rank sends the fully reduced chunk to circulate the final values around the ring. Total data sent = $(N - 1) \times (S / N)$.
4. **Total Volume:** Summing both phases yields $2 \times \frac{N - 1}{N} S$. As $N \to \infty$, the total transmitted data approaches $2S$, completely independent of cluster size $N$. Every network link is fully utilized with zero idle workers, achieving theoretical bandwidth optimality.

---

## Question 2: In Floyd-Warshall, why must the loop over the intermediate vertex k be the outermost loop?
**Answer:**
- Floyd-Warshall is dynamic programming where $DP[k][i][j]$ represents the shortest distance from $i$ to $j$ considering only vertices in the subset $\{0, 1, \dots, k\}$ as potential intermediates.
- The recurrence $DP[k][i][j] = \min(DP[k-1][i][j], DP[k-1][i][k] + DP[k-1][k][j])$ requires that all shortest paths using intermediates $\{0, \dots, k-1\}$ are already finalized before considering $k$.
- If $k$ were placed in the inner loop, path calculations for $(i, j)$ would attempt to use intermediate $k$ before paths between $(i, k)$ and $(k, j)$ had been relaxed through earlier intermediates, generating incorrect shortest paths.
