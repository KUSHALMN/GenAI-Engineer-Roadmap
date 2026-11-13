# 🎯 Technical Interview Questions — Day 16: Collectives & Sliding Window Maximum

## Question 1: How does All-to-All communication differ from All-Reduce, and why does MoE token dispatch make All-to-All the primary network bottleneck?
**Answer:**
1. **Communication Pattern:**
   - **All-Reduce:** Every GPU has a tensor of size $S$, and all GPUs compute and receive the identical reduced sum of all tensors ($2 \frac{N-1}{N} S$).
   - **All-to-All:** Every GPU has a distinct piece of data for every other GPU. In MoE token dispatch, GPU $i$ routes token activations to GPU $j$ where expert $E_j$ resides, and receives tokens for its local experts from all other GPUs.
2. **Network Saturation:**
   - All-to-All generates an $N \times N$ all-pairs traffic matrix across the entire cluster.
   - If experts are distributed across physical nodes connected by InfiniBand (50 GB/s) rather than intra-node NVLink (900 GB/s), network bisection bandwidth saturates, stalling GPU Tensor Cores. Consequently, production MoE designs (DeepSeek-V3, Mixtral) constrain expert parallel groups to intra-node NVLink domains or use specialized hierarchical dispatchers.

---

## Question 2: In LeetCode 239, explain why a Monotonic Deque maintains the maximum in O(1) amortized time per step.
**Answer:**
- **Strictly Decreasing Invariant:** The deque stores indices whose values are strictly decreasing (`nums[deque.peekFirst()]` is always the maximum in the window).
- **Amortized Analysis:**
  - Each index $i \in [0, N-1]$ enters the deque at the back (`offerLast`) exactly once.
  - An index is removed from the front if it expires from the window, and removed from the back if a newly incoming element is strictly larger.
  - Because each element is pushed once and popped at most once, total deque operations across the entire array of length $N$ is at most $2N$.
  - Amortized cost per window step is strictly $O(1)$, yielding an overall optimal $O(N)$ runtime.
