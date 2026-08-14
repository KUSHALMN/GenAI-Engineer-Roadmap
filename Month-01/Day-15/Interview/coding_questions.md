# Coding Questions — Day 15

## Java — Binary Tree

### Max Depth (Easy)
```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return Math.max(maxDepth(root.left), maxDepth(root.right)) + 1;
}
```

### Inorder Traversal (Easy)
```java
private void dfs(TreeNode node, List<Integer> result) {
    if (node == null) return;
    dfs(node.left, result);
    result.add(node.val);
    dfs(node.right, result);
}
```

## Python — Hybrid Retrieval

### Keyword scoring
```python
keywords = set(question.lower().split())
score = len(keywords & set(chunk.lower().split()))
```

### Hybrid merge with deduplication
```python
seen, merged = set(), []
for chunk in semantic + keyword:
    if chunk not in seen:
        seen.add(chunk)
        merged.append(chunk)
return merged[:TOP_K]
```
