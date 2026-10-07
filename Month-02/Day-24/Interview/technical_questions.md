# 🎯 Day 24 Technical Interview Questions & Answers

## 1. What are the core pillars of GenAI Observability, and how do they differ from classical software observability?
**Answer:**
Classical observability focuses on the three pillars: **Metrics, Logs, and Traces (M.E.L.T)** covering CPU, memory, HTTP status codes, and network latency.
In GenAI systems, observability must expand to include:
1. **Semantic Tracing**: Tracking execution across chunking, embedding generation, vector database search, query rewriting, and LLM reasoning steps.
2. **Token Economics**: Real-time tracking of input/output token counts, model tier pricing, and cache hit ratios.
3. **Quality & Groundedness Metrics**: Real-time hallucination scoring, RAG triad scores (Context Relevance, Groundedness, Answer Faithfulness), and toxicity.
4. **LLM Performance Metrics**: Time-to-First-Token (TTFT), tokens per second (tok/s), and inter-token latency for streaming APIs.

---

## 2. Why is Distributed Context Propagation (`request_id` / `trace_id`) critical in async RAG architectures?
**Answer:**
A single user request to a RAG system involves asynchronous background tasks (vector embeddings, multi-query retrieval, parallel reranking, and guardrail validation).
Without distributed context propagation (using mechanisms like Python's `contextvars` or OpenTelemetry span context):
- Logs from concurrent queries get interleaved, making post-incident debugging impossible.
- Correlating token costs and latency bottlenecks to a specific tenant or user session fails.
- Trace trees break across asynchronous boundaries (`asyncio.gather` or message queues).

---

## 3. How do you implement a Monotonic Queue for Sliding Window Maximum in $O(N)$ time?
**Answer:**
A standard sliding window approach evaluating the maximum across $K$ elements takes $O(N \cdot K)$ in the worst case, or $O(N \log K)$ with a max-heap.
A Monotonic Queue uses a double-ended queue (`Deque`) storing array indices:
1. When inserting index $i$, evict any indices smaller than $nums[i]$ from the back of the deque, maintaining a strictly decreasing order.
2. Evict any index from the front if it falls outside the active sliding window range $(i - k + 1)$.
3. The element at the front of the deque is guaranteed to be the maximum of the current window.
Because each element is inserted and evicted at most once, the total time complexity across $N$ elements is strictly $O(N)$.
