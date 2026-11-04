# Interview Questions: Retrieval Metrics & Bitmask Dynamic Programming

### Q1: Why is NDCG@K often preferred over Recall@K in cross-encoder reranker evaluation?
**Answer**:
Recall@K treats relevance as binary (0 or 1) and is completely **position-insensitive** within the top-$K$ window: whether the most relevant document appears at Rank 1 or Rank 10, Recall@10 is identical.
In contrast, **NDCG@K** applies a logarithmic position discount $\frac{1}{\log_2(\text{rank} + 1)}$: placing the best document at Rank 1 scores significantly higher than placing it at Rank 10. This aligns with LLM attention dynamics, where earlier context passages receive higher prompt weighting.

### Q2: Why is the state in Bitmask Assignment DP represented by the mask alone?
**Answer**:
The number of assigned tasks is directly equal to the number of set bits (count of 1s) in `mask`:
$$\text{worker} = \text{Integer.bitCount}(\text{mask})$$
Because the current worker index is deterministically inferred from the mask itself, the DP state does not require a 2D table `dp[worker][mask]`; a 1D array `dp[mask]` of size $2^N$ completely encapsulates the state space.

### Q3: How does Bitmask DP reduce complexity from factorial $\mathcal{O}(N!)$ to exponential $\mathcal{O}(N \cdot 2^N)$?
**Answer**:
In naive backtracking, exploring permutations evaluates all $N!$ orderings. However, many sub-paths reach the exact same subset of assigned tasks (e.g. assigning Worker 0 to Task A and Worker 1 to Task B reaches the same remaining task set as Worker 0 to B and Worker 1 to A). By memoizing the subproblem `dp[mask]`, each of the $2^N$ subset states is computed only once, iterating through $N$ transitions per state.
