# Interview Questions: Hybrid Search & Stream Median

### Q1: Why does raw score summation fail when combining BM25 and vector search?
**Answer**:
BM25 yields unbounded non-negative scores ($[0, \infty)$) that scale with IDF and query length, while cosine similarities from dense embeddings are strictly bounded in $[-1, 1]$ (or $[0, 1]$ with normalized dot product). Adding unnormalized scores results in BM25 dominating dense semantics, or vice versa depending on query length. Solutions include Reciprocal Rank Fusion (RRF) which relies only on rank order, or min-max normalization.

### Q2: What is the optimal constant $k$ in RRF, and how does it prevent top ranks from dominating?
**Answer**:
The standard constant $k=60$ (introduced by Cormack et al.) smooths the impact of top ranks. Without $k$ (i.e. $1/rank$), rank 1 receives a score of 1.0 while rank 2 receives 0.5 (a 50% drop). With $k=60$, rank 1 is $1/61 \approx 0.01639$ and rank 2 is $1/62 \approx 0.01612$, preventing a single outlier high-rank from completely overwhelming consistent moderate rankings across retrievers.

### Q3: How do two heaps maintain the running median in $\mathcal{O}(\log N)$ insert time?
**Answer**:
A max-heap stores the smaller half $\lfloor N/2 \rfloor + 1$ elements and a min-heap stores the remaining $\lfloor N/2 \rfloor$ larger elements. Each new element is first routed to max-heap, transferred to min-heap, and re-balanced. The median is either the top of max-heap (odd count) or the average of both tops (even count), computed in $\mathcal{O}(1)$.
