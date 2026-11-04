# Interview Questions: Graph vs. Vector Search & Bipartite Graphs

### Q1: Why does a query like "Find all suppliers connected to companies acquired by Entity X" fail on pure vector search?
**Answer**:
Vector search only measures similarity between the query text and individual text passages. It cannot execute multi-table relational joins or recursive pointer-following across entities. Answering this question requires traversing:
`Entity X -[ACQUIRED]-> Company Y -[CONTRACTED_WITH]-> Supplier Z`.
Only graph databases or relational join queries can reliably compute this multi-hop path without hallucinating unconnected entities.

### Q2: What is the fundamental property linking bipartite graphs and cycle lengths?
**Answer**:
A graph is bipartite **if and only if it contains NO odd-length cycles**.
If a cycle has an odd number of vertices (e.g. a triangle with 3 vertices), alternating between two colors inevitably causes two adjacent vertices on the cycle to have the same color. If all cycles are even, two colors are always sufficient.

### Q3: How does the BFS 2-coloring algorithm handle disconnected graph components?
**Answer**:
The outer loop iterates through all vertices $0$ to $n-1$. If a vertex has not yet been colored (`color[i] == 0`), a new BFS traversal is launched with that vertex as the root of a new connected component. This guarantees that all isolated subgraphs are checked for odd cycles.
