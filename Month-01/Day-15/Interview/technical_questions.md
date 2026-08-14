# Technical Questions — Day 15

## Hybrid Search RAG

**Q: What is the difference between semantic and keyword retrieval?**
- Semantic: uses vector embeddings — finds conceptually similar chunks even without exact word match
- Keyword: counts word overlap — finds chunks with exact matching terms

**Q: Why is hybrid retrieval better than either alone?**
Semantic misses exact terms, keyword misses meaning. Hybrid combines both — better recall overall.

**Q: How does your hybrid merger work?**
Semantic results are listed first (higher priority), keyword results fill gaps. Deduplication via a set ensures no chunk appears twice. Final list is trimmed to TOP_K.

**Q: What is the time complexity of keyword retrieval?**
O(n * m) where n = number of chunks, m = number of keywords. Linear scan over all stored chunks.

## Binary Tree DSA

**Q: What are the three DFS traversal orders?**
- Inorder (L→Root→R): gives sorted output for BST
- Preorder (Root→L→R): used to copy/serialize a tree
- Postorder (L→R→Root): used to delete a tree or evaluate expressions

**Q: How does max depth work recursively?**
Base case: null node returns 0. Recursive case: max(left depth, right depth) + 1.

**Q: Time and space complexity of tree DFS?**
Time: O(n) — visits every node once. Space: O(h) — call stack depth equals tree height.
