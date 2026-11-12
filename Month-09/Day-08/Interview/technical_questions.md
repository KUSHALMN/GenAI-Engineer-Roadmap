# 🎯 Technical Interview Questions — Day 08: 3D Parallelism & Topological Sort

## Question 1: How do engineers decide the exact dimension factors for DP, TP, and PP when scaling a 405B parameter model across 16,384 H100 GPUs?
**Answer:**
1. **TP Dimension (Always intra-node $\le 8$):** Tensor parallelism requires high-frequency communication ($>900\text{ GB/s}$). It is strictly constrained to the number of GPUs per chassis sharing NVLink (typically $TP = 8$). Cross-node TP is avoided due to InfiniBand latency stalls.
2. **PP Dimension (Minimizing Bubble Overhead):** Pipeline parallelism allows fitting remaining parameters across nodes. Setting $PP = 8$ or $16$ partitions the 405B model weights into ~25B to 50B chunks per stage. Micro-batches $M$ must be chosen such that $M \ge 4 \times PP$ to keep the pipeline bubble $\frac{PP - 1}{PP - 1 + M} < 20\%$.
3. **DP Dimension (Remaining Cluster Capacity):** Data parallelism scales throughput across all remaining nodes:
   $$DP = \frac{\text{Total GPUs}}{TP \times PP} = \frac{16,384}{8 \times 16} = 128$$
   Combined with ZeRO-1/FSDP within each DP replica group, global batch size scales into millions of tokens per step.

---

## Question 2: In Kahn's Algorithm for Topological Sort, how does the queue maintain the invariant and detect cycles?
**Answer:**
- **Invariant:** A vertex is enqueued if and only if its in-degree is zero, meaning all of its prerequisite dependencies have already been placed into the topological ordering.
- **Cycle Detection:** If a directed graph contains a cycle, no vertex in that cycle will ever reach an in-degree of zero because each node has at least one unresolved incoming dependency from within the cycle.
- Consequently, vertices in the cycle are never enqueued, and the final processed count will be strictly less than $V$, immediately signaling a cycle.
