# 📅 Day 05 Notes — Cross-Encoder Rerankers & BST Validation

## 🧠 What I Learned
1. **Multi-Stage Retrieval Funnel:**
   - Stage 1 (Fast Recall): BM25 + Vector Bi-Encoder $\rightarrow$ retrieve top 50-100 candidates.
   - Stage 2 (Precision Rerank): Cross-Encoder (e.g. `bge-reranker-large` / Cohere Rerank) $\rightarrow$ rerank down to top 3-5.
   - Stage 3 (Context Compression): Sentence-level extractor prunes extraneous text to minimize prompt token bloat.
2. **BST Invariants:**
   - BST condition is global: all descendants in the left subtree must be strictly less than the ancestor.
   - Inorder traversal converts BST validation into an array monotonicity check.
3. **Recover BST (LC 99):**
   - Inorder traversal allows detecting the two swapped elements in $\mathcal{O}(N)$ time and $\mathcal{O}(H)$ space by finding where `prev.val > curr.val`.
