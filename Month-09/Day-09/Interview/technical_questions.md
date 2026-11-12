# 🎯 Technical Interview Questions — Day 09: FlashAttention & KMP Algorithm

## Question 1: How does FlashAttention achieve a 2–4x speedup over standard Attention when it performs the exact same mathematical computations?
**Answer:**
1. **The Memory Wall & Roofline Model:** Standard attention is not compute-bound; it is severely **memory bandwidth-bound** (IO-bound).
2. **Intermediate HBM R/W Eliminaton:**
   - Standard attention materializes the full $N \times N$ attention matrix $S = Q K^T$ into High Bandwidth Memory (HBM, ~3 TB/s), then reads it back to compute Softmax, writes $P = \text{softmax}(S)$ back to HBM, and reads $P$ again to compute $O = P V$. For sequence length $N = 32k$, $N^2$ requires gigabytes of HBM traffic.
3. **SRAM Tiling & Online Softmax:** FlashAttention loads blocks of $Q, K, V$ into on-chip **SRAM cache** (~19 TB/s on H100), computes attention incrementally using the Online Softmax trick, and writes *only* the final $N \times d$ output $O$ directly to HBM. Memory reads/writes drop from $O(N^2)$ to $O(N)$, speeding up execution purely through IO reduction.

---

## Question 2: In the KMP Algorithm, what does the LPS (Longest Prefix Suffix) array store, and why does it prevent backtracking the haystack pointer i?
**Answer:**
- **LPS Definition:** `lps[j]` stores the length of the longest proper prefix of `needle[0..j]` that is also a suffix of `needle[0..j]`.
- **Zero Backtracking:**
  - In naive string matching, a mismatch forces the text pointer $i$ to reset back to $i - j + 1$, resulting in $O(N \times M)$ worst-case time.
  - In KMP, if a mismatch occurs after matching $j$ characters, the LPS value `lps[j-1]` tells us the exact length of the prefix that already matches the current suffix of the text.
  - The text pointer $i$ never retreats; the pattern pointer $j$ simply falls back to `lps[j-1]`, guaranteeing strictly $O(N + M)$ linear time.
