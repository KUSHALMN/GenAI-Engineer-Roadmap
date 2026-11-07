# Day 19: Technical Interview Preparation — KV Cache Math & Producer-Consumer

### Q1: Why did modern LLMs transition from Multi-Head Attention (MHA) to Grouped-Query Attention (GQA)?
**Answer:**
In MHA, each query head has its own Key and Value head ($H_{KV} = H_Q$), leading to massive KV cache memory footprints during decoding that throttle maximum batch sizes. GQA groups multiple query heads (e.g. 8 query heads share 1 KV head), reducing KV cache memory by $8\times$ with virtually zero degradation in model output quality.

### Q2: Why is `ArrayBlockingQueue` preferred over `LinkedBlockingQueue` in latency-sensitive serving pipelines?
**Answer:**
`ArrayBlockingQueue` allocates its internal backing array upfront, eliminating runtime object allocations. `LinkedBlockingQueue` creates a new `Node` wrapper object on every `put()`, generating significant GC garbage and memory fragmentation under high throughput.
