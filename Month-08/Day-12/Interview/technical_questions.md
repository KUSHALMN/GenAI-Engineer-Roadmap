# 🎯 Technical Interview Questions — Day 12: Drift Detection & Graphs

### 1. Contrast Data Drift with Concept Drift in Generative AI systems.
**Answer:**
- **Data Drift (Covariate Shift):** The distribution of user queries or inputs changes over time (e.g., users start asking about a new product released yesterday), while the true underlying relationship remains unchanged.
- **Concept Drift:** The statistical relationship between input queries and the correct answer changes over time (e.g., "What is the prime interest rate?" changes every quarter). This requires updating the knowledge corpus or fine-tuning weights.

### 2. What is the space complexity of DFS on a grid of dimensions $M \times N$?
**Answer:**
In the worst-case (a grid filled entirely with '1's), the call stack can grow up to $O(M \times N)$ recursive frames. For massive grids, BFS with an explicit queue or Disjoint Set Union (DSU) prevents stack overflow errors.
