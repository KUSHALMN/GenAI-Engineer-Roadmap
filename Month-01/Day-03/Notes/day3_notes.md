# Day 3 Notes — GenAI Engineer Roadmap

## Topics Learned

### RAG (Retrieval Augmented Generation)
- **RAG** — combines a retrieval system with an LLM to answer questions from external documents
- **Chunking** — splitting large documents into smaller overlapping pieces for better retrieval
- **Overlap** — shared words between chunks to preserve context at boundaries

---

## Python Practice

### Chunk Text
- Split text into fixed-size word chunks with overlap
- Overlap prevents losing context at chunk boundaries
- Used in RAG pipelines before storing in vector DB

### Cosine Similarity (from scratch)
- Implemented dot product and magnitude manually
- `cosine_similarity = dot(a,b) / (|a| * |b|)`
- Range: 0 (no similarity) → 1 (identical direction)

---

## DSA (Java)

### Best Time to Buy and Sell Stock — LeetCode #121
- Approach: Greedy O(n)
- Track minimum price seen so far, compute max profit at each step

### Longest Common Prefix — LeetCode #14
- Approach: Horizontal Scanning O(n*m)
- Start with first string as prefix, shrink until all strings match

### Longest Substring Without Repeating Characters — LeetCode #3
- Approach: Sliding Window + HashSet O(n)
- Expand right pointer, shrink left when duplicate found

---

## AI Project — PDF Similarity Search

- Loaded PDF text using `pypdf`
- Chunked text with overlap for better context
- Stored chunks in ChromaDB as embeddings
- Queried by semantic similarity using Sentence Transformers

---

## Key Takeaway
RAG = Chunk → Embed → Store → Retrieve → Generate. Chunking strategy directly impacts retrieval quality.
