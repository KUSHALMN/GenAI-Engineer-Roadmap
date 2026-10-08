# 💬 Day 05: Rerankers & Validate BST Interview Questions

### Q1: Compare Bi-Encoders and Cross-Encoders in production search architectures.
**Answer:**
- **Bi-Encoder:** Encodes query $q$ and document $d$ into dense vectors independently: $u = f(q), v = f(d)$. Similarity is a fast dot product $\langle u, v \rangle$. Documents can be pre-embedded and indexed into an approximate nearest neighbor (ANN) vector database. Scales to billions of documents in milliseconds.
- **Cross-Encoder:** Jointly encodes the pair: $[CLS] \ q \ [SEP] \ d \ [SEP]$ through all transformer self-attention layers. Token-to-token attention interactions between query and document tokens are fully captured. It produces significantly higher accuracy, but has $\mathcal{O}(N)$ inference cost per document and cannot be pre-computed.
- **Standard Pipeline:** Bi-Encoder retrieves top 100 candidate documents $\rightarrow$ Cross-Encoder reranks them down to top 5.

---

### Q2: Why is checking only `node.left.val < node.val < node.right.val` insufficient for validating a BST?
**Answer:**
Because the BST property applies to the *entire* subtree, not just immediate children. For example, in a tree where root is 5, right child is 8, and right child's left grandchild is 3:
Locally, $3 < 8$, but globally, 3 is in the right subtree of 5, which violates $3 > 5$.
Validation requires carrying monotonic bounds: $\text{low} < \text{node.val} < \text{high}$.

---

### Q3: How do we handle integer overflow edge cases in LeetCode 98?
**Answer:**
If the tree contains `Integer.MIN_VALUE` or `Integer.MAX_VALUE`, integer-typed bounds cannot distinguish between an uninitialized bound and a boundary value. We use `long` bounds initialized to `Long.MIN_VALUE` and `Long.MAX_VALUE`, or use nullable `Integer` references.
