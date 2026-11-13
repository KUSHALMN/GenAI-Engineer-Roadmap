# 🎯 Technical Interview Questions — Day 12: Sequence Parallelism & Hierholzer's Algorithm

## Question 1: How does Megatron-LM Sequence Parallelism (SP) eliminate activation memory redundancy without introducing any additional communication operations?
**Answer:**
1. **The TP Redundancy Problem:** In standard Tensor Parallelism, activations for LayerNorm, Dropout, and residual connections are replicated identically across all $TP$ GPUs. For sequence length $s=8192$, this replicated activation state accounts for up to 30% of total training memory.
2. **Replacing All-Reduce with All-Gather and Reduce-Scatter:**
   - In standard TP, RowParallelLinear ends with an **All-Reduce** (which internally consists of a Reduce-Scatter followed by an All-Gather).
   - In Sequence Parallelism, RowParallelLinear performs *only* the **Reduce-Scatter**, dispersing the output so each GPU receives only a slice of sequence length $s / TP$.
   - The subsequent LayerNorm and Dropout execute on this sharded slice with zero redundancy.
   - Before the next ColumnParallelLinear, an **All-Gather** reassembles the full sequence.
3. **Zero Extra Communication:** Because one All-Reduce ($2 \frac{N-1}{N} S$) is mathematically split into one Reduce-Scatter ($\frac{N-1}{N} S$) and one All-Gather ($\frac{N-1}{N} S$), total communication volume is **identical** to standard TP, while reducing LayerNorm/Dropout activation memory by $(1 - 1/TP) = 87.5\%$ for $TP=8$.

---

## Question 2: In Hierholzer's Algorithm for finding an Eulerian Path, why must vertices be added to the result path in post-order (on backtracking)?
**Answer:**
- **Dead-End Pitfall:** In a directed graph, greedily traversing edges can lead into a sub-tour or dead-end vertex before visiting all other edges in the graph.
- **Post-Order Reversal Invariant:** When a vertex has no more outgoing edges to explore, it must be the end of the current trail or a closed cycle. Adding the vertex to the front of a linked list (`itinerary.addFirst(u)`) upon backtracking guarantees that any detached sub-cycles are spliced into the main Eulerian tour at the exact vertex where the cycle originated, producing a globally valid path traversing every directed edge exactly once.
