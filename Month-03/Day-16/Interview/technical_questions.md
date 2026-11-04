# Interview Questions: Citation Attribution & Prim's Algorithm

### Q1: How do you prevent citation hallucination in prompt engineering?
**Answer**:
1. **Numbered Bracket Injection**: Explicitly format context chunks as:
   `[Doc 1] Title: ... Content: ...`
2. **Negative Constraint & Abstention**: Include the rule:
   `"Only cite documents provided in the context using [Doc N]. Do NOT invent citation numbers. If a claim cannot be verified from the context, state 'I do not have enough evidence'."`
3. **Programmatic Post-Verification**: A regex/NLI verification layer audits the generated answer before presenting it to the user.

### Q2: Why is Prim's algorithm preferred over Kruskal's for dense graphs?
**Answer**:
For dense graphs where $E \approx V^2$:
- Kruskal's requires sorting $V^2$ edges, taking $\mathcal{O}(V^2 \log(V^2)) = \mathcal{O}(V^2 \log V)$.
- Prim's with a Fibonacci heap runs in $\mathcal{O}(E + V \log V) = \mathcal{O}(V^2)$.
- Prim's with adjacency matrix runs in $\mathcal{O}(V^2)$ without any heap overhead, outperforming Kruskal's on complete graphs.

### Q3: What happens in Prim's algorithm if the graph is disconnected?
**Answer**:
If the graph is disconnected, the visited counter (`visitedCount`) will never reach $V$ because vertices in other disconnected components cannot be reached by incident edges. The algorithm terminates early and reports that no spanning tree exists (returns $-1$).
