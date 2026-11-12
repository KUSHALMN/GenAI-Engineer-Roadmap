# 🎯 Technical Interview Questions — Day 06: ZeRO Optimization & Wildcard Trie

## Question 1: Detail the 16 bytes-per-parameter breakdown in mixed-precision Adam training and explain how ZeRO-1, ZeRO-2, and ZeRO-3 partition them.
**Answer:**
1. **Model State Memory Breakdown (16 Bytes / parameter):**
   - **FP16 Model Weights:** 2 bytes (used in forward/backward compute).
   - **FP16 Gradients:** 2 bytes (computed during backward pass).
   - **FP32 Master Weights:** 4 bytes (accumulates weight updates in high precision).
   - **FP32 Adam Momentum ($m_t$):** 4 bytes.
   - **FP32 Adam Variance ($v_t$):** 4 bytes.
   - *Sum:* $2 + 2 + 4 + 4 + 4 = 16$ bytes per parameter.
2. **ZeRO Partitioning Stages:**
   - **ZeRO-1 ($P_{os}$):** Partitions the 12 bytes of FP32 optimizer states across $N_d$ data-parallel GPUs. Memory = $2 + 2 + 12 / N_d$ bytes/param ($4\times$ memory reduction for large $N_d$). Communication overhead = 0% extra.
   - **ZeRO-2 ($P_{os+g}$):** Partitions both optimizer states and gradients. Memory = $2 + (2 + 12) / N_d$ bytes/param ($8\times$ reduction). Communication overhead = 0% extra (replaces All-Reduce with Reduce-Scatter).
   - **ZeRO-3 ($P_{os+g+p}$):** Partitions all 16 bytes linearly ($16 / N_d$ bytes/param). Parameters are gathered dynamically via All-Gather right before layer execution and freed immediately after, incurring a 50% communication overhead.

---

## Question 2: In LeetCode 211 (Wildcard Trie search), what is the worst-case time complexity when searching a string of '.' characters?
**Answer:**
- **Worst-Case Branching:** If the search string consists solely of $M$ wildcards `"."` and the Trie contains all $26^M$ possible combinations of lowercase English characters, the recursive search must visit every child at every level.
- **Complexity:** $O(26^M)$ where $M$ is the length of the search string.
- **Pruning in Practice:** For practical dictionaries, most Trie branches are empty (`node.children[i] == null`), so recursion terminates early, yielding sub-millisecond lookups.
