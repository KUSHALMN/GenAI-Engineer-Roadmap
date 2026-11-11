# 🎯 Technical Interview Questions — Day 10: Experiment Tracking & BSTs

### 1. What parameters are essential for 100% reproducible RAG retrieval experiments?
**Answer:**
1. **Document Corpus Version:** Exact Git commit or dataset snapshot hash.
2. **Chunking Configuration:** Strategy (Recursive, Markdown), chunk size (tokens), and overlap.
3. **Embedding Model & Dimensions:** Exact model weights identifier and normalization flag.
4. **Index & Distance Metric:** HNSW parameters (`M`, `efConstruction`) and metric (Cosine, Dot Product).
5. **Retrieval & Reranking:** Top-K retrieved, Cross-Encoder reranker model ID, and score cutoffs.

### 2. Why is checking only `node.val > node.left.val` and `node.val < node.right.val` insufficient for LC 98 Validate BST?
**Answer:**
A BST requires that **all** nodes in the left subtree are strictly less than the root, and **all** nodes in the right subtree are strictly greater. A local parent-child check fails on subtrees where a right descendant violates an ancestor's bound (e.g., `5 -> left: 1, right: 6 (left: 3, right: 7)` where `3 < 5` is invalid in the right subtree). Passing `(min, max)` boundaries preserves global invariants.
