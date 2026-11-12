# 📝 Notes — Day 02: Pretraining DataLoaders & Bellman-Ford

- **Binary Token Packing:** `struct.pack('<H', token_id)` uses exactly 2 bytes per token for vocabularies $\le 65535$, cutting storage by 75% compared to JSON/plaintext.
- **Bellman-Ford Invariant:** After $i$ relaxation iterations, the algorithm guarantees the shortest path using at most $i$ edges.
- **Negative Cycles:** A standard $V$-th iteration that yields further relaxation proves the existence of a negative cycle reachable from the source.
