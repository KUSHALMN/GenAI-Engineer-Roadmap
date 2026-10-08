# 📅 Day 04 Notes — Hybrid Dense-Sparse Retrieval & Tree BFS

## 🧠 What I Learned
1. **Sparse vs Dense Tradeoffs:**
   - Sparse (BM25): Fast, exact keyword matching, handles rare acronyms/IDs, explainable.
   - Dense: Semantic capture, multilingual mapping, soft concept matching.
2. **Reciprocal Rank Fusion (RRF):**
   - Eliminates need for score scale normalization between unbounded BM25 and normalized cosine similarity.
   - Robust constant $k=60$ dampens the penalty difference between top ranks.
3. **Tree BFS Queue Invariants:**
   - Capturing `queue.size()` locks the level horizon.
   - Zigzag traversal can be optimized using `LinkedList.addFirst()` vs `addLast()` without reversing post-hoc.
