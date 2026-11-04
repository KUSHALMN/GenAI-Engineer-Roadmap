# Interview Questions: Contextual Compression & Floyd-Warshall

### Q1: What is the main risk of over-compressing context before LLM generation?
**Answer**:
1. **Context Fragmentation**: Stripping surrounding sentences may eliminate vital qualifiers (e.g., "However, this only applies in dry environments" or "Except when $x < 0$").
2. **Coreference Rupture**: A sentence containing "It achieved 99% accuracy" becomes incomprehensible if the preceding sentence identifying "The ResNet-50 model" was pruned away.

### Q2: Why is the outer loop in Floyd-Warshall over intermediate vertex $k$?
**Answer**:
Floyd-Warshall is a dynamic programming algorithm where the subproblem state $dist^{(k)}[i][j]$ represents the shortest path from $i$ to $j$ using only vertices from the subset $\{0, 1, \dots, k\}$ as internal waypoints.
If $k$ were the innermost loop, the algorithm would compute paths considering single intermediate vertices in isolation without chaining multiple intermediate vertices together.

### Q3: When should Floyd-Warshall be used instead of running Dijkstra $V$ times?
**Answer**:
- If the graph has **negative edge weights** (without negative cycles), Dijkstra cannot be used; Floyd-Warshall handles negative weights correctly.
- For **dense graphs** ($E \approx V^2$), running Dijkstra with binary heaps takes $\mathcal{O}(V \cdot E \log V) = \mathcal{O}(V^3 \log V)$, which is slower than Floyd-Warshall's clean cache-friendly $\mathcal{O}(V^3)$ array iterations.
