# Recruiter Questions — Day 15

**Q: What did you build today?**
Added hybrid search to the RAG chatbot — it now runs both semantic (vector) and keyword retrieval, merges results, deduplicates, and returns the best chunks. This improves answer quality compared to either strategy alone.

**Q: What is hybrid search and why does it matter?**
Hybrid search combines vector similarity (semantic) with keyword matching. Semantic search finds conceptually related content, keyword search finds exact terms. Together they cover more retrieval scenarios.

**Q: What tree problems have you solved?**
Binary tree inorder traversal and maximum depth — both using DFS recursion. Key insight: tree problems almost always reduce to a base case (null = 0 or empty) and a recursive case combining left and right subtree results.

**Q: How do you structure a production RAG system?**
Separate concerns into modules: loading, splitting, embedding, vector store, retrieval strategies, prompt building, and pipeline orchestration. Each module is independently testable and swappable.
