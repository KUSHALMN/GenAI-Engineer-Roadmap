# 📅 Day 21: Document Deletion & Lowest Common Ancestor

## 🎯 Deliverables
- **AI Engine**: `AI/delete_document_pipeline.py`
  - Distributed cascade deletion coordinator.
  - Multi-tier cleanup across Blob storage, relational DB, vector index, and cache.
  - Tombstone state audit and stale-vector verification.
- **Java DSA**: `DSA/LowestCommonAncestor.java`
  - LeetCode 236: Lowest Common Ancestor in Binary Tree $\mathcal{O}(N)$ post-order DFS.
  - LeetCode 235: Lowest Common Ancestor in BST $\mathcal{O}(H)$ time, $\mathcal{O}(1)$ space.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Deletion Coordinator
python Month-03/Day-21/AI/delete_document_pipeline.py

# Java DSA
javac Month-03/Day-21/DSA/LowestCommonAncestor.java
java -cp Month-03/Day-21/DSA LowestCommonAncestor
```
