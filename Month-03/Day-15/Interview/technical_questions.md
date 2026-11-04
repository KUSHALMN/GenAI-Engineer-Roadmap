# Interview Questions: Multi-Tenant Metadata Filtering & Kruskal's MST

### Q1: Why is Single-Index Multi-Tenancy risky without hard pre-filtering?
**Answer**:
Without mandatory pre-filtering at the database query engine level, confidential chunks from Tenant B can inadvertently appear in retrieved context sent to Tenant A's LLM prompt (cross-tenant data leakage). Hard pre-filtering enforces SQL `WHERE tenant_id = :current_tenant` or Qdrant `filter: {must: [{key: "tenant_id", match: {value: "tenant_a"}}]}` before distance scoring occurs.

### Q2: Compare Kruskal's Algorithm with Prim's Algorithm for Minimum Spanning Trees.
**Answer**:
- **Kruskal's**:
  - Edge-centric: Sorts all edges globally and adds edges greedily if they don't form cycles (via DSU).
  - Time complexity: $\mathcal{O}(E \log E)$.
  - Best for **sparse graphs** ($E \ll V^2$).
- **Prim's**:
  - Vertex-centric: Grows a connected component from a single root node using a PriorityQueue.
  - Time complexity: $\mathcal{O}((V + E) \log V)$ with binary heap.
  - Best for **dense graphs** ($E \approx V^2$).

### Q3: Why is sorting edges $\mathcal{O}(E \log E)$ equivalent to $\mathcal{O}(E \log V)$?
**Answer**:
In any simple graph, $E \le V^2$.
Thus, $\log(E) \le \log(V^2) = 2 \log(V)$.
Therefore, $\mathcal{O}(E \log E) = \mathcal{O}(E \cdot 2 \log V) = \mathcal{O}(E \log V)$.
