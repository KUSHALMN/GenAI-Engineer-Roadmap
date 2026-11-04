# Interview Questions: RAG Ablation & Interval DP

### Q1: What is the trade-off between Recall@K and latency when adding a cross-encoder reranker?
**Answer**:
- **Recall Gain**: A cross-encoder reranks the top 50 candidates retrieved by fast bi-encoder/BM25 using full cross-attention. Empirically, this increases Top-3 precision and MRR by 15–25% by catching subtle keyword negations and exact syntactic relationships.
- **Latency Cost**: Cross-encoders run full transformer forward passes over $K$ pairs ($50$ queries $\times 512$ tokens), adding 40–120ms of compute latency. In real-time chat, teams must determine whether this latency budget fits within the overall SLO ($< 1$ second).

### Q2: Why is "which balloon bursts LAST" the breakthrough insight for LeetCode 312?
**Answer**:
If we try to decide which balloon bursts *first*, the remaining balloons become adjacent to each other. Bursting balloon $x$ immediately alters the neighbors of $x-1$ and $x+1$, creating cross-interval dependencies that break the optimal substructure required for independent dynamic programming subproblems.
By defining $k$ as the balloon that bursts *last* in interval $[i, j]$, all other balloons in $[i, j]$ are already gone; therefore, $k$'s neighbors are deterministically $i-1$ and $j+1$, decoupling the subproblems $[i, k-1]$ and $[k+1, j]$.

### Q3: How do you loop over intervals in Interval DP to ensure subproblems are solved before larger intervals?
**Answer**:
The outer loop MUST iterate over the **length of the interval** (`len` from $1$ to $N$).
Within that length, iterate over starting index $i$ and ending index $j = i + len - 1$.
This guarantees that whenever we compute an interval of length $L$, all sub-intervals of length $< L$ have already been calculated and stored in the DP table.
