# Interview Questions: Document Deletion & LCA Algorithm

### Q1: How do you implement GDPR-compliant deletion in an approximate nearest neighbor (HNSW) vector index?
**Answer**:
In HNSW graphs, deleting a node requires restructuring the multi-layer proximity edges connecting its neighbors, which can trigger graph fragmentation if done synchronously in real-time.
*Best Practice*:
1. **Soft Tombstone**: Immediately mark the point payload as `deleted = true` so pre-filters exclude it from all active query traversals.
2. **Periodic Vacuum / Compaction**: Background worker runs periodic vector index compaction (e.g. Qdrant vacuum optimizer) that rebuilds graph layers without the tombstoned vectors.

### Q2: What is the post-order DFS logic behind LeetCode 236 (Lowest Common Ancestor)?
**Answer**:
In a bottom-up post-order traversal:
1. If the current node matches $p$ or $q$, return current node immediately.
2. Search left and right subtrees.
3. If both `left != null` and `right != null`, it means $p$ and $q$ are located in separate subtrees of the current node; therefore, the current node is their lowest common ancestor.
4. If only one subtree returned non-null, pass that non-null node upward (both targets lie within that subtree).

### Q3: Why is LCA in a BST solvable in $\mathcal{O}(H)$ time and $\mathcal{O}(1)$ space?
**Answer**:
The BST ordering property guarantees that if both $p$ and $q$ are strictly smaller than the current node, their LCA must reside in the left subtree. If both are strictly greater, their LCA must reside in the right subtree. The very first node where paths diverge (or where current node equals $p$ or $q$) is guaranteed to be the LCA, allowing a simple iterative `while` loop with no recursion stack.
