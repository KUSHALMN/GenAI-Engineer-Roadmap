# Day 22: Coding Interview Questions & Answers
## Focus: Connected Components, Multi-Source BFS, and Graph Matrix Traversal

---

### Q1: In LeetCode 994 (*Rotting Oranges*), why must we track `freshCount` and why is running independent BFS passes from each rotten orange sub-optimal?

**Answer:**
1. **Flaw of Independent BFS Passes**:
   - If we ran a standard BFS from each rotten orange independently, we would have to record distance matrices for every rotten orange and take the minimum across all of them:
     $$\text{Time Complexity} = O(K \times M \times N)$$
     where $K$ is the number of rotten oranges (up to $M \times N$), yielding worst-case $O((MN)^2)$ time.
2. **Optimality of Multi-Source BFS**:
   - Enqueueing all $K$ rotten oranges at $T = 0$ guarantees that each cell is visited **at most once** as the closest wave reaches it.
   - **Time Complexity**: Exactly $O(M \times N)$.
3. **Role of `freshCount`**:
   - If `freshCount == 0` initially, we can immediately return `0` without queue iterations.
   - If `freshCount > 0` after the BFS queue empties, unreachable oranges exist $\implies$ return `-1`.

---

### Q2: Compare solving *Number of Provinces* (LeetCode 547) via DFS vs Disjoint Set Union (Union-Find). What are the space-time trade-offs?

**Answer:**
1. **DFS on Adjacency Matrix**:
   - **Time Complexity**: $O(N^2)$ because we examine every cell $(i, j)$ in the $N \times N$ matrix.
   - **Space Complexity**: $O(N)$ for the `visited` array + recursion stack.
2. **Disjoint Set Union (DSU)**:
   - **Time Complexity**: $O(N^2 \cdot \alpha(N))$ because we iterate over the upper triangle of the matrix ($N(N-1)/2$ pairs) and execute `union()`. Since $\alpha(N) \le 4$, this is effectively $O(N^2)$.
   - **Space Complexity**: $O(N)$ for `parent` and `rank` arrays without any recursion call stack.
3. **Dynamic Streaming Graphs**:
   - If edges are arriving dynamically in a real-time stream (e.g. social network connections added one by one), **DSU is strictly superior** because adding an edge takes $O(\alpha(N)) \approx O(1)$ incremental time without re-running full graph traversals.
