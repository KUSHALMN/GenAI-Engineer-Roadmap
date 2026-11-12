# 📝 Notes — Day 03: DDP Ring All-Reduce & Floyd-Warshall

- **Gradient Bucketing:** DDP organizes parameter gradients into contiguous memory buffers (~25MB buckets) to trigger Ring All-Reduce asynchronously while earlier layer backward passes are still executing.
- **Floyd-Warshall Complexity:** Strictly $O(V^3)$ time and $O(V^2)$ space; ideal for dense graphs with $V \le 500$.
- **Graph Infinity Guard:** Initialize non-edges with `1e9` rather than `Integer.MAX_VALUE` to avoid arithmetic overflow when computing `dist[i][k] + dist[k][j]`.
