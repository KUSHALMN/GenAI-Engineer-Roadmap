# 📝 Notes — Day 04: Tensor Parallelism & Prim's Algorithm

- **Why Not Cross-Node TP?** Each token in TP requires low-latency synchronization ($< 5\mu s$). Inter-node ethernet/InfiniBand latency ($15\text{--}50\mu s$) creates intolerable compute stalls; TP is almost universally restricted to intra-node NVLink (8 GPUs).
- **Prim's Complexity:** With an adjacency matrix and PriorityQueue, complexity is $O(V^2 \log V)$ for complete graphs. With Fibonacci heap or distance array tracking, Prim runs in $O(V^2)$ or $O(E \log V)$.
