# 💻 Day 29 Coding Interview Questions: Serialize and Deserialize Binary Tree

### Problem: Serialize and Deserialize Binary Tree (LeetCode 297 - Hard / FAANG Classic)
**Key Insight (BFS Level-Order)**:
1. **Serialization**:
   - Use a Queue. Enqueue root.
   - While queue is not empty: pop node.
   - If node is not null, append `node.val` and enqueue `left` and `right`.
   - If node is null, append `"null"`.
2. **Deserialization**:
   - Split the serialized string by `,`.
   - The first token is the root.
   - Use a pointer or index `idx` stepping by 2 for each parent popped from the reconstruction queue to assign its left and right children.

**Complexity Analysis**:
- **Time Complexity**: $O(N)$ for both serialization and deserialization, visiting every node and null sentinel exactly once.
- **Space Complexity**: $O(N)$ for queue storage at the widest level ($N/2$ leaf nodes in a balanced tree).
