# 💬 Day 04: Hybrid Search & Level Order Traversal Interview Questions

### Q1: Why do enterprise RAG pipelines combine BM25 sparse search with dense embeddings?
**Answer:**
Dense semantic embeddings excel at capturing conceptual intent and synonym relationships (e.g. mapping "cardiovascular condition" to "heart illness"), but they struggle with out-of-vocabulary technical identifiers, product SKUs, exact acronyms, error codes, and specific entity names. BM25 sparse search uses exact inverted index term frequencies with saturation, excelling where embeddings fail. Combining them mitigates the weaknesses of both.

---

### Q2: How does Reciprocal Rank Fusion (RRF) work and why is it preferred over raw score addition?
**Answer:**
BM25 scores are unbounded positive numbers (typically between 0 and 50+ depending on document length and term IDF), whereas cosine similarity scores from dense embeddings range strictly between -1.0 and 1.0. Directly adding them requires delicate score calibration and normalization (e.g. MinMax or Softmax), which is sensitive to distribution drift.
RRF is rank-based rather than score-based:
$$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + \text{rank}_m(d)}$$
Where $k$ is a constant (typically 60). RRF guarantees robust, distribution-independent combination without calibration.

---

### Q3: In Binary Tree BFS, why do we capture `queue.size()` before the inner level loop?
**Answer:**
Because new children are actively enqueued (`queue.offer(curr.left)`) during the level iteration. If we evaluated `queue.size()` dynamically in the loop condition, the loop would continue into the next level instead of terminating at the current depth boundary. Freezing `int levelSize = queue.size()` guarantees that each batch corresponds strictly to one tree depth.
