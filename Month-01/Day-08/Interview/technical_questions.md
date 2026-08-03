# Technical Questions — Day 08

## RAG & Vector Search

**Q: What is the difference between semantic search and keyword search?**
> Keyword search matches exact words. Semantic search uses embeddings to find results by meaning — even if the exact words don't match.

**Q: Why do we chunk documents in RAG?**
> LLMs have a limited context window. Chunking splits large documents into smaller pieces so only the most relevant chunks are passed to the LLM, keeping the context focused and within token limits.

**Q: What is the difference between chunk_size and overlap?**
> chunk_size controls how many words per chunk. overlap is the number of shared words between consecutive chunks to preserve context at boundaries.

**Q: What is lazy loading in Python?**
> Loading a resource only when it's first needed, not at startup. Used in embedding.py to load the model only once on first call, saving memory and startup time.

**Q: What is `get_or_create_collection` in ChromaDB?**
> Safely gets an existing collection or creates a new one if it doesn't exist. Prevents errors on re-runs.

---

## Python & Architecture

**Q: Why separate embedding and vector_store into different files?**
> Single Responsibility Principle — each module does one thing. Makes code easier to test, maintain, and swap out (e.g., replace ChromaDB with Pinecone without touching embedding logic).

**Q: What is a global variable in Python and when is it used?**
> A variable defined at module level. Used for singleton patterns like a shared model instance (`_model = None`) to avoid reloading on every function call.

---

## Binary Search

**Q: Why use `mid = left + (right - left) / 2` instead of `(left + right) / 2`?**
> To prevent integer overflow. When left and right are large integers, their sum can exceed the max int value in Java.

**Q: What is the difference between `left <= right` and `left < right` in binary search?**
> `left <= right` — used when returning index directly (standard search). `left < right` — used when converging to a single element (e.g., find minimum, first bad version).
