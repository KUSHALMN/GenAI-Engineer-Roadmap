# Day 31: Technical Interview Preparation — Month 05 Capstone & Ring Buffer

### Q1: Summarize the architectural pillars of Month 05 (Fine-Tuning, Model Adaptation & Inference).
**Answer:**
1. **Data Engineering:** Dataset schemas (ChatML), strict deduplication, prompt masking, and synthetic generation without model collapse.
2. **PEFT & Adaptation:** Parameter freezing, low-rank decomposition (LoRA), and 4-bit NormalFloat (QLoRA) enabling training on consumer GPUs.
3. **Inference Optimization:** Separating compute-bound prefill from bandwidth-bound decode; PagedAttention virtual block memory management.
4. **Serving Architecture:** Continuous batching eliminating bubble padding; SSE token streaming with client cancellation detection.
5. **Production Operations:** Gateway routing, semantic caching, TTL eviction, and capacity budgeting.

### Q2: Why are lock-free Ring Buffers (e.g. LMAX Disruptor) used in ultra-low latency trading and AI serving engines?
**Answer:**
Traditional queues use locks or CAS retry loops that cause CPU cache-line bouncing (cache contention). A Ring Buffer uses pre-allocated contiguous memory and sequential sequence counters (`AtomicLong.lazySet`), avoiding locks, allocations, and cache misses to achieve tens of millions of operations per second with predictable latency.
