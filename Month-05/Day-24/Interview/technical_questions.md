# Day 24: Technical Interview Preparation — Model Gateway & Compare-And-Swap (CAS)

### Q1: What capabilities must an Enterprise Model Gateway possess?
**Answer:**
1. **Unified Schema:** OpenAI-compatible API mapping across local and third-party models.
2. **Circuit Breaking & Automatic Fallback:** Route to alternative providers on HTTP 5xx or latency spikes.
3. **Usage & Budget Accounting:** Centralized token metering and spend enforcement.
4. **Semantic Caching:** Cache responses for exact or similar queries to eliminate duplicate costs.

### Q2: How does hardware Compare-And-Swap (CAS) achieve thread safety without locks?
**Answer:**
CAS is an atomic CPU instruction (e.g. `cmpxchg` on x86). It compares the contents of a memory location to an expected value, and only if they match, modifies the location to a new value. If another thread mutated the value concurrently, CAS returns false, allowing the thread to retry in a loop without context-switching to OS mutexes.
