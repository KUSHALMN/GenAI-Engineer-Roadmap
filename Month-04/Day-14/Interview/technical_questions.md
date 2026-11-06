# Day 14: Technical Interview Preparation — Trajectory Evaluation & LCS

### Q1: Why is final output evaluation insufficient for benchmarking agent systems?
**Answer:**
An agent might produce the correct final answer through a flawed, dangerous, or excessively expensive trajectory (e.g. attempting 15 hallucinated API calls, exposing PII, or querying redundant endpoints). Trajectory evaluation audits the *path taken*, rewarding step efficiency and penalizing policy violations.

### Q2: How can LCS be reconstructed from the 2D DP matrix?
**Answer:**
Start at `dp[m][n]`. If `text1[i-1] == text2[j-1]`, this character is part of the LCS; append it to our result and move diagonally to `dp[i-1][j-1]`. Otherwise, move in the direction of the larger neighbor (`dp[i-1][j]` or `dp[i][j-1]`). Reverse the resulting characters when cell `[0][0]` is reached.
