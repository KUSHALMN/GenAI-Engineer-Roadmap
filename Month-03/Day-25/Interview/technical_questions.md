# Interview Questions: Retrieval Caching & Sparse Table

### Q1: What is the difference between an Exact Cache and a Semantic Vector Cache (e.g. GPTCache)?
**Answer**:
- **Exact Cache**: Requires strict equality on the hash key. Zero risk of false-positive matches, but has a low hit rate on natural language variations ("What is X?" vs "Can you define X?").
- **Semantic Vector Cache**: Embeds the incoming query and performs a nearest-neighbor vector search in a cache index. If similarity $\ge 0.96$, it serves the cached result.
  - *Risk*: Risk of semantic false positives (e.g., "What was company profit in 2023?" vs "What was company profit in 2024?" might have a 0.95 embedding similarity but require completely different factual answers).

### Q2: Why can Sparse Table answer Range Minimum Queries in $\mathcal{O}(1)$ time while Segment Tree takes $\mathcal{O}(\log N)$?
**Answer**:
Sparse Table leverages the **idempotence** of the `min` operator:
$$\min(A, B) = \min(A, A, B)$$
Because duplicated elements do not alter the minimum, any range $[L, R]$ can be completely covered by two overlapping blocks of length $2^k$, each precalculated in the table.
In contrast, Segment Tree divides the range into disjoint canonical segments, which may require visiting up to $2 \lceil \log_2 N \rceil$ nodes.

### Q3: Why can't a Sparse Table answer Range Sum Queries in $\mathcal{O}(1)$?
**Answer**:
Addition is **not idempotent**: $A + B \ne A + A + B$. Overlapping the two power-of-2 ranges would sum the overlapping intersection twice, producing an incorrect total. Range Sum on a Sparse Table would require combining disjoint powers of 2, taking $\mathcal{O}(\log N)$ (making Fenwick or Segment Tree strictly superior for dynamic sums).
