# Day 21: Technical Interview Preparation — PagedAttention & CompletableFuture

### Q1: What problem in traditional LLM serving does PagedAttention solve?
**Answer:**
Traditional serving frameworks pre-allocated contiguous memory for each sequence's maximum length ($L_{max}$), leading to 60-80% memory waste due to internal fragmentation (unreserved tokens) and external fragmentation. PagedAttention divides the KV cache into fixed-size pages (e.g. 16 tokens), mapping virtual logical sequence tokens to non-contiguous physical blocks on the GPU, near-eliminating memory waste and doubling throughput.

### Q2: Why is `CompletableFuture` superior to standard `Future`?
**Answer:**
Standard `Future` is blocking: calling `.get()` halts the thread until completion. `CompletableFuture` provides non-blocking, event-driven reactive chaining (`thenApply`, `thenCompose`, `thenCombine`), exceptional handling (`exceptionally`), and timeout fallback guarantees.
