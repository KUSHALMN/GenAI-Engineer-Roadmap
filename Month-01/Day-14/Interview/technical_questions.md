# Technical Questions — Day 14

## Multi-Document RAG

**Q: How do you ingest multiple PDFs?**
Loop over files in `sample_documents/`, call `ingest()` for each `.pdf` file. All chunks land in the same ChromaDB collection.

**Q: How does cross-document retrieval work?**
ChromaDB retrieves the top-k most semantically similar chunks regardless of which document they came from.

**Q: Why remove prompt_builder.py?**
For simple use cases, building the prompt inline in `rag_pipeline.py` reduces file count without losing clarity.

## Sliding Window DSA

**Q: When to use fixed vs variable sliding window?**
- Fixed: window size k is given — Maximum Average Subarray
- Variable: window size depends on a condition — Longest Substring Without Repeating Characters

**Q: What is the time complexity of sliding window?**
O(n) — each element is added and removed from the window at most once.

**Q: How is sliding window better than brute force?**
Brute force checks all subarrays O(n²). Sliding window reuses previous computation by only adding the new element and removing the old one.
