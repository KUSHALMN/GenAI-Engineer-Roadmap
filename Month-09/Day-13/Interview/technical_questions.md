# 🎯 Technical Interview Questions — Day 13: RingAttention & Valid Parentheses

## Question 1: How does RingAttention scale sequence length to millions of tokens without causing memory out-of-bounds or network saturation?
**Answer:**
1. **Context Parallel Sequence Partitioning:** The global sequence $S$ (e.g. 1,000,000 tokens) is split into $N$ equal blocks ($S / N$). Each GPU stores only its assigned query chunk $Q_i$, key chunk $K_i$, and value chunk $V_i$. VRAM requirements drop from $O(S)$ to $O(S / N)$.
2. **Circular Ring Communication:**
   - In step $k$, GPU $i$ computes attention between its local $Q_i$ and the currently held $K_{\text{curr}}, V_{\text{curr}}$ block using FlashAttention's Online Softmax rescaling.
   - Concurrently, via non-blocking asynchronous peer-to-peer CUDA streams (`torch.distributed.isend` / `irecv`), GPU $i$ sends its $K, V$ blocks to rank $(i + 1) \% N$ and receives from $(i - 1 + N) \% N$.
3. **Compute-Communication Overlap:** Since computing attention on a block of size $S / N \times d$ takes more time than transferring the block across NVLink/InfiniBand, communication latency is 100% hidden behind compute. Exact full attention over arbitrary sequence lengths scales linearly with GPU count.

---

## Question 2: In LeetCode 32 (Longest Valid Parentheses), why does a single forward pass fail in O(1) space, and why is a reverse pass required?
**Answer:**
- In a forward pass (left-to-right), tracking `left` and `right` counts detects valid substrings when `left == right`, and resets when `right > left` (unmatched closing bracket).
- However, if the string has excess opening brackets (e.g., `"(()"`), `left` is always greater than `right`, so `left == right` is never triggered and the answer remains 0.
- A **reverse pass** (right-to-left) symmetrically counts brackets and resets when `left > right` (unmatched opening bracket).
- Running both passes ensures all valid substrings are captured in $O(N)$ time with strictly $O(1)$ auxiliary space.
