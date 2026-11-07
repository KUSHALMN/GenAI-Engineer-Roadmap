# Day 30: Technical Interview Preparation — Project 5 Release & Collections Mock

### Q1: Summarize the end-to-end lifecycle of adapting and serving an open-weights LLM.
**Answer:**
1. **Data Preparation:** Clean, deduplicate, filter, and format into ChatML JSONL; ensure zero test set leakage.
2. **Fine-Tuning:** Use QLoRA (NF4 4-bit base + LoRA adapter) with cosine LR decay and prompt masking.
3. **Artifact Packaging:** Merge LoRA adapter weights or export adapter checkpoint alongside metadata manifest.
4. **Serving & Inference:** Deploy via vLLM with PagedAttention and continuous batching over SSE streaming endpoints.
5. **Observability & Guardrails:** Enforce model gateway routing, semantic caching, and token budget limits.

### Q2: Why is `ArrayDeque` preferred over `Stack` in Java?
**Answer:**
`java.util.Stack` inherits from the synchronized `Vector` class, incurring lock overhead on every operation. `ArrayDeque` is non-synchronized, provides faster array-backed pushing and popping, and avoids vector locking latency.
