# Technical Questions — Day 09

## RAG Pipeline Architecture

**Q: What is the role of `rag_pipeline.py`?**
> It's the orchestrator — it calls ingest (load → chunk → embed → store) and query (retrieve → build prompt → LLM). It hides all complexity from app.py, keeping the entry point clean.

**Q: What is the role of `retriever.py`?**
> It abstracts the retrieval step — given a query, it returns the most relevant chunks from the vector store. It can also return distance scores to evaluate retrieval quality.

**Q: What is the role of `prompt_builder.py`?**
> It constructs the final prompt sent to the LLM — combining the system instruction, retrieved context chunks (labeled), and the user question.

**Q: Why label chunks as [Chunk 1], [Chunk 2] in the prompt?**
> It helps the LLM understand that multiple separate pieces of context are provided, reducing confusion when chunks contain different information.

**Q: What is a distance score in ChromaDB?**
> A measure of how far (dissimilar) a chunk is from the query embedding. Lower distance = more relevant. Used to evaluate retrieval quality.

---

## Two Pointers

**Q: Why merge from the end in Merge Sorted Array (LC #88)?**
> Merging from the front would overwrite elements in nums1 before they're used. Merging from the end uses the empty space at the back of nums1 safely — no extra array needed.

**Q: What is the Two Pointers pattern?**
> Using two indices (left/right or slow/fast) to traverse an array efficiently. Reduces O(n²) brute force to O(n). Used in palindrome check, merge sorted arrays, container with most water, etc.

---

## Python

**Q: What is the difference between a module and a package?**
> A module is a single `.py` file. A package is a directory with an `__init__.py` containing multiple modules.

**Q: What does `include=["documents", "distances"]` do in ChromaDB?**
> Tells ChromaDB to return both the document text and the similarity distances in the query result.
