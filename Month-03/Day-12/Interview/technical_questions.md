# Interview Questions: HyDE & Dijkstra Algorithm

### Q1: Why can HyDE work even when the hypothetical document contains factual errors?
**Answer**:
Dense embedding models map texts into thematic neighborhoods based on lexical style, domain concepts, and syntactic composition rather than discrete truth verification. As long as the hypothetical document is *topically and linguistically aligned* with the domain, its embedding vector resides in the correct cluster of the corpus space.

### Q2: Why does Dijkstra fail on graphs with negative edge weights?
**Answer**:
Dijkstra assumes that adding an edge to a known shortest path can never decrease the total path length (greedy monotonicity property). Once a node is marked visited/settled, Dijkstra guarantees its shortest distance will not be updated. A negative edge breaks this assumption because a path visiting more vertices could end up having a smaller total weight. Bellman-Ford or SPFA must be used instead.

### Q3: How does Dijkstra achieve $\mathcal{O}((V + E) \log V)$ with a binary heap?
**Answer**:
Each vertex is extracted from the PriorityQueue at most once ($\mathcal{O}(V \log V)$).
Each edge is relaxed at most once, which adds a new distance entry to the heap ($\mathcal{O}(E \log V)$).
Summing both gives $\mathcal{O}((V + E) \log V)$.
