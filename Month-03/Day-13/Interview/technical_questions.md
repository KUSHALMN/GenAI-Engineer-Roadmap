# Interview Questions: Cross-Encoder Rerankers & Bellman-Ford

### Q1: Why can't we use a cross-encoder directly across our entire 10-million chunk corpus?
**Answer**:
A cross-encoder requires passing $[CLS] + query + [SEP] + doc$ through all transformer layers for every candidate. For a 10-million document corpus, computing 10 million cross-attention inferences would take hours for a single query. A bi-encoder pre-computes fixed vectors offline, reducing search to an approximate nearest neighbor (ANN) dot product taking $\le 10$ milliseconds.

### Q2: Why does Bellman-Ford run $V - 1$ times to guarantee shortest paths in a DAG / directed graph?
**Answer**:
In any simple path with $V$ vertices, there are at most $V - 1$ edges. In each round of edge relaxation, paths of length $k$ edges are extended to valid shortest paths of length $k + 1$. Thus, after $V - 1$ passes, all possible shortest paths without cycles are fully relaxed.

### Q3: How does the $(V)$-th pass in Bellman-Ford detect negative weight cycles?
**Answer**:
If a graph contains no negative cycles, all shortest paths have at most $V - 1$ edges and distances cannot decrease further. If any edge $(u, v, w)$ can still be relaxed on the $V$-th pass ($dist[u] + w < dist[v]$), it mathematically proves that a negative-weight cycle exists that can infinitely reduce path weights.
