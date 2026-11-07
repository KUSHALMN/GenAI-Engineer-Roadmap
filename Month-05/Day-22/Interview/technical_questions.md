# Day 22: Technical Interview Preparation — SSE Streaming & ReadWriteLock

### Q1: What happens on the model server if an HTTP client disconnects midway through a 500-token stream?
**Answer:**
Without active cancellation detection, the GPU server continues auto-regressively decoding all 500 tokens, wasting VRAM and Tensor Core compute. Production servers use async cancellation hooks (e.g. `request.is_disconnected()`) to abort generation immediately and evict the request's KV cache.

### Q2: When is `ReentrantReadWriteLock` preferred over standard `ReentrantLock`?
**Answer:**
In read-heavy scenarios (e.g. 95% reads, 5% writes such as reading model metadata or cached embeddings). Multiple reader threads can execute concurrently without blocking each other, only pausing when an exclusive write lock is required.
