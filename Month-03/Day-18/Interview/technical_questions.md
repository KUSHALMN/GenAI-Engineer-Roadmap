# Interview Questions: GraphRAG & Tarjan's SCC Algorithm

### Q1: When is GraphRAG worth the indexing cost vs standard Vector RAG?
**Answer**:
- **Use GraphRAG**: When users ask high-level exploratory, holistic, or relationship-heavy queries across thousands of documents (e.g., "Summarize all legal liabilities across subsidiaries" or "How are entities A and B connected across 5 hops?").
- **Avoid GraphRAG**: Simple FAQ lookup, code search, or single-document extraction where the 10x–50x LLM token cost during indexing cannot be economically justified.

### Q2: How does Tarjan's algorithm differ from Kosaraju's for SCCs?
**Answer**:
- **Tarjan's Algorithm**:
  - Requires only **one DFS pass** $\mathcal{O}(V + E)$.
  - Maintains `disc`, `low`, and an explicit recursion stack to identify roots of SCCs on the fly.
- **Kosaraju's Algorithm**:
  - Requires **two DFS passes**:
    1. First DFS on original graph to determine finish times (fill a stack).
    2. Transpose all graph edges ($G^T$).
    3. Second DFS on reversed graph in decreasing order of finish time.

### Q3: What is the significance of the `onStack[v]` check in Tarjan's algorithm?
**Answer**:
When exploring an edge $(u, v)$, if $v$ is already visited (`disc[v] != -1`), we must check whether $v$ is currently in the active recursion stack (`onStack[v] == true`).
If it is on the stack, $(u, v)$ is a **back-edge** to an ancestor in the current SCC component.
If it is NOT on the stack, $v$ belongs to an already completed SCC discovered earlier in the DFS traversal and must NOT update `low[u]`.
