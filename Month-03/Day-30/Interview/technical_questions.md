# Interview Questions: Production RAG v2 Release & Capstone Mock

### Q1: Walk me through the failure modes of a RAG pipeline from ingestion to response generation.
**Answer**:
1. **Ingestion**: Parser drops tables or loses reading order; chunking cuts mid-sentence across vital definitions.
2. **Embedding**: Out-of-vocabulary technical jargon or acronyms mapped into incorrect vector clusters.
3. **Retrieval**: Vocabulary mismatch (pure vector fails on exact ID numbers; pure BM25 fails on synonyms).
4. **Context Window**: Lost-in-the-middle effect when 20 chunks are stuffed into context without reranking or compression.
5. **Generation**: Citation hallucination or sycophancy where the LLM agrees with a false premise in the user query despite contradictory retrieved evidence.

### Q2: Why is a doubly linked list used alongside a hash map in LRU Cache design?
**Answer**:
- A **Hash Map** provides $\mathcal{O}(1)$ average key lookup.
- A **Doubly Linked List** allows $\mathcal{O}(1)$ removal of an arbitrary node (since each node holds pointers to both `prev` and `next`), and $\mathcal{O}(1)$ insertion to the head (most recently used) and deletion from the tail (least recently used).
Using a singly linked list would require $\mathcal{O}(N)$ traversal to find the previous node before deletion.

### Q3: Why does a Min-Heap of size $K$ solve the Kth Largest Element problem in $\mathcal{O}(N \log K)$?
**Answer**:
By maintaining a min-heap bounded by size $K$, the heap always stores the $K$ largest elements seen so far.
The smallest of these $K$ largest elements is at the root (`peek()`).
When a new element arrives, we push it and poll the smallest if size exceeds $K$.
After scanning all $N$ elements, the root of the min-heap is guaranteed to be the $K$-th largest element in the entire array, using only $\mathcal{O}(K)$ extra memory.
