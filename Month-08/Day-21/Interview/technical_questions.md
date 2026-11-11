# 🎯 Technical Interview Questions — Day 21: Cost Observability & Java Collections

## Question 1: How do you design an LLM cost attribution engine for thousands of microservices with hard SLA and budget circuit breakers?
**Answer:**
1. **Header-based Tenant Metadata:** Inbound requests pass `X-Tenant-ID`, `X-Department-ID`, and `X-Cost-Center` metadata via API gateways.
2. **Streaming Token Extraction:** Modern LLM APIs return `usage.prompt_tokens` and `usage.completion_tokens` upon chunk completion or header trailers. The gateway asynchronously dispatches these to a real-time Redis or ClickHouse time-series datastore.
3. **Sliding-Window Tripwires:** An in-memory token bucket or quota counter evaluates departmental spend against configured burn rates. If the 80% threshold is reached, Slack/PagerDuty webhooks alert owners. If the 100% threshold is breached, non-critical traffic is shed or downgraded to cheaper models (e.g., Gemini Flash or 8B quant models).

---

## Question 2: Why is ArrayDeque preferred over Stack and LinkedList in Java for queue/stack operations?
**Answer:**
- `java.util.Stack` inherits from `Vector`, which synchronizes every method, incurring unnecessary lock acquisition overhead in single-threaded or executor worker contexts.
- `LinkedList` allocates a `Node` object for every element added, creating significant GC pressure, 24 bytes of pointer overhead per entry, and poor CPU cache locality.
- `ArrayDeque` uses a resizable contiguous ring-buffer array, zero pointer overhead per element, cache-friendly memory layout, and $O(1)$ amortized insertion and removal.
