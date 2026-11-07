# Day 27: Technical Interview Preparation — Failure Handling & Semaphores

### Q1: What strategies handle context window overflow when a user prompt exceeds model limits?
**Answer:**
1. **Sliding Window / Head-Tail Truncation:** Retain the first $K$ system tokens and last $N$ turns, discarding middle history.
2. **Context Summarization:** Use a fast 3B model to summarize the previous turns into a compact paragraph.
3. **Chunked RAG:** Chunk the overflow context, embed it, and retrieve only the top relevant sections.

### Q2: How does a `Semaphore` differ from a `ReentrantLock` in Java?
**Answer:**
- `ReentrantLock`: A mutex with single ownership (only 1 thread can hold it; the thread that locks it must unlock it). Supports reentrancy.
- `Semaphore`: Maintains a set of $N$ permits. Any thread can acquire or release permits. Does not enforce thread ownership, making it ideal for resource pools and concurrency throttling.
