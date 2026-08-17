# 💻 Coding Interview Questions — Day 17

### Problem 1 (Java): Validate Binary Search Tree (LeetCode #98)
**Task:** Given the root of a binary tree, determine if it is a valid binary search tree (BST).
**Key Concept:** Pass dynamic lower and upper bounds `(min, max)` recursively through each subtree.
```java
public boolean isValidBST(TreeNode root) {
    return validate(root, null, null);
}
private boolean validate(TreeNode node, Integer min, Integer max) {
    if (node == null) return true;
    if ((min != null && node.val <= min) || (max != null && node.val >= max)) return false;
    return validate(node.left, min, node.val) && validate(node.right, node.val, max);
}
```

---

### Problem 2 (Java): Binary Tree Level Order Traversal (LeetCode #102)
**Task:** Given the root of a binary tree, return the level order traversal of its nodes' values.
**Key Concept:** BFS queue where `levelSize = queue.size()` processes node boundaries per depth level.

---

### Problem 3 (Python): Reciprocal Rank Fusion (RRF)
**Task:** Given two ranked lists of retrieved documents, compute combined RRF scores and return the top sorted order.
```python
def rrf(list_a, list_b, k=60):
    scores = {}
    for r_list in [list_a, list_b]:
        for rank, doc in enumerate(r_list, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
```
