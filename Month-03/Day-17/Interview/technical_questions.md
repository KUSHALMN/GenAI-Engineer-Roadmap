# Interview Questions: Multi-Hop RAG & Topological Sort

### Q1: What is the error propagation problem in Multi-Hop RAG?
**Answer**:
If Hop 1 extracts an incorrect or hallucinated intermediate entity (e.g., attributing transformers to Meta instead of Google), Hop 2 executes a conditioned retrieval on false premises (querying "CEO of Meta"), leading to cascading factual failures. Mitigations include threshold confidence checking at every hop and self-consistency voting across multiple decomposition paths.

### Q2: Why does Kahn's algorithm detect cycles in a directed graph?
**Answer**:
Kahn's algorithm initializes a queue with all vertices having in-degree 0. As vertices are popped, the in-degrees of their outgoing neighbors are decremented. In a graph with a directed cycle, every vertex in the cycle has at least one incoming edge belonging to the cycle; thus, none of their in-degrees can ever reach 0. They are never enqueued, and `processedCount < V` flags the cycle.

### Q3: How do you choose between Kahn's BFS and DFS for Topological Sort?
**Answer**:
- **Kahn's BFS**: Naturally handles cycle detection via in-degree tracking without recursion stack overhead; directly yields the order from root prerequisites to dependent tasks.
- **DFS**: Uses a 3-state coloring (Unvisited = 0, Visiting = 1, Visited = 2) to detect back-edges. Yields the reverse topological order when pushing nodes to a stack upon recursive return.
