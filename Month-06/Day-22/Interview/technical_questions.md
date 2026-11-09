# Technical Interview Preparation — Cross-Modal Evaluation & 2D DP
1. Mean Reciprocal Rank (MRR) vs NDCG: MRR evaluates binary relevance based on first relevant hit ($1 / rank$). NDCG evaluates graded relevance with logarithmic rank discount.
2. Longest Common Subsequence Recurrence: Match adds 1 to diagonal $dp[i-1][j-1]$; mismatch takes max of top $dp[i-1][j]$ and left $dp[i][j-1]$.
