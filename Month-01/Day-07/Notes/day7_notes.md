# Day 7 Notes — GenAI Engineer Roadmap

## Topics Learned

### PDF RAG Chatbot
- Full RAG pipeline: PDF → Extract → Chunk → Embed → Store → Retrieve → Answer
- Two chunking strategies: word-based and sentence-based
- ChromaDB for vector storage and semantic retrieval
- Groq LLaMA 3.3 70B for answer generation

### Python Utilities
- `@timer` decorator — measure function execution time
- `@retry` decorator — auto-retry on failure with delay
- `flatten()` — recursively flatten nested lists
- `batch()` — split list into fixed-size batches

---

## DSA (Java)

### Longest Substring Without Repeating Characters — LeetCode #3
- Approach: Sliding Window + HashSet O(n)
- Expand right, shrink left when duplicate found
- Track max window size

### Best Time to Buy and Sell Stock — LeetCode #121
- Approach: Greedy O(n)
- Track minimum price seen so far
- Compute profit at each step, update max

---

## Interview Prep
- Reviewed technical questions: RAG, embeddings, FastAPI, SQL
- Practiced coding questions: Two Sum, FizzBuzz, Palindrome, Flatten
- Prepared recruiter answers: projects, strengths, goals

---

## Key Takeaway
A PDF RAG chatbot is the most practical GenAI project to showcase — it combines embeddings, vector search, chunking, and LLM generation in one real-world application.
