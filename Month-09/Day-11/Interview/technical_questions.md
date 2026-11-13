# 🎯 Technical Interview Questions — Day 11: MoE Routing & Edit Distance

## Question 1: How does Mixture-of-Experts (MoE) scale model parameter capacity without proportionally increasing inference FLOPs, and why is an auxiliary load balancing loss required?
**Answer:**
1. **Sparse Activation:** In dense models, every parameter is activated for every token. In MoE (e.g., Mixtral 8x7B, DeepSeek-V3), feed-forward layers are replaced by $E$ independent expert networks, but a learned router selects only the Top-$K$ experts (typically $K=2$) per token. A model with 47B total parameters activates only ~13B parameters per token, retaining the compute footprint of a 13B model with the expressive capacity of a 47B model.
2. **Routing Collapse Phenomenon:** Left unconstrained, the router quickly experiences "winner-take-all" mode collapse: a few experts receive all tokens, while other experts starve and receive zero gradients.
3. **Auxiliary Balancing Loss:** To prevent collapse, models introduce an auxiliary loss $\mathcal{L}_{\text{aux}} = \alpha \cdot E \sum_{i=1}^E f_i \cdot P_i$, where $f_i$ is the actual fraction of tokens assigned to expert $i$, and $P_i$ is the average softmax probability routed to expert $i$. This loss is minimized when tokens and probabilities are distributed uniformly across all experts.

---

## Question 2: In LeetCode 72 (Edit Distance), how does the space complexity reduce from O(M * N) to O(min(M, N))?
**Answer:**
- Standard DP fills a matrix `dp[m+1][n+1]` where `dp[i][j]` depends strictly on:
  - `dp[i-1][j-1]` (diagonal: replace / match)
  - `dp[i-1][j]` (top: delete from word1)
  - `dp[i][j-1]` (left: insert into word1)
- Because computing row $i$ requires only values from row $i-1$ and row $i$, we can maintain a single 1D array of size $N+1$.
- A scalar variable `prevDiag` stores the old diagonal value `dp[i-1][j-1]` before `dp[j]` is updated in-place.
- By swapping the words if $M < N$, we ensure the 1D buffer size is strictly $\min(M, N) + 1$, optimizing both RAM footprint and CPU L1 cache locality.
