# 🎯 Technical Interview Questions — Day 11: Online Quality & Heaps

### 1. How do you design an online quality feedback loop without introducing latency into streaming responses?
**Answer:**
Separate the generation path from the telemetry and feedback path asynchronously:
1. Emit streaming response chunks directly over SSE or WebSockets to the client.
2. Provide a unique `interaction_id` in the response header/metadata envelope.
3. When the user clicks thumbs-up/down or submits correction text, send a lightweight background POST to `/api/v1/telemetry/feedback` which enqueues to Redis/Kafka, avoiding any API thread blocking.

### 2. Compare $O(N \log K)$ Min-Heap vs. $O(N)$ Quickselect for finding the Kth largest element.
**Answer:**
- **Min-Heap ($O(N \log K)$):** Ideal for streaming data where elements arrive continuously and total size $N$ is unknown or cannot fit in memory. Space is $O(K)$.
- **Quickselect ($O(N)$ average):** Faster in-place algorithm for static arrays, but degrades to $O(N^2)$ worst-case without randomized pivot selection.
