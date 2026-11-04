# Interview Questions: Multi-Query Retrieval & Disjoint Set Union

### Q1: What is the main latency cost of Multi-Query Retrieval and how do you optimize it?
**Answer**:
Multi-query generates $k$ queries (e.g., 3–5 queries), which would sequentially take $k \times$ retrieval time.
*Optimization*:
1. **Parallel Vector Retrieval**: Execute the $k$ vector queries concurrently using asynchronous client connections (`asyncio.gather` or thread pools).
2. **Batch Embedding**: Pass all $k$ queries in a single batch tensor call to the embedding API/model.
3. **Early Deduplication**: Discard duplicates before passing candidates to downstream expensive rerankers.

### Q2: What is the time complexity of Disjoint Set Union with Path Compression and Union by Rank?
**Answer**:
The amortized time per operation is $\mathcal{O}(\alpha(N))$, where $\alpha$ is the Inverse Ackermann function.
For all practical values of $N$ ($N \le 10^{80}$, the number of atoms in the observable universe), $\alpha(N) \le 4$. Therefore, DSU operations run in effectively constant time $\mathcal{O}(1)$.

### Q3: When should you use DSU over DFS/BFS for connected components?
**Answer**:
DSU is strictly superior for **dynamic connectivity** (graphs where edges are added incrementally over time). With DSU, checking connectivity or adding an edge is $\mathcal{O}(\alpha(N))$ without re-traversing the graph. DFS/BFS requires $\mathcal{O}(V + E)$ from scratch every time an edge is inserted.
