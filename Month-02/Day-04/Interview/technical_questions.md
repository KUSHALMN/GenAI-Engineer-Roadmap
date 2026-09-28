# Day 35 (Month 02 - Day 04): Interview Questions
## Focus: LLM Caching, Cost Optimization, LRU Cache

---

### Q1: Why use SHA-256 for LLM cache keys instead of the raw prompt string?

**Answer:**
1. **Fixed size**: SHA-256 always produces a 64-char hex key regardless of prompt length — consistent HashMap performance.
2. **Collision resistance**: Cryptographically negligible collision probability across billions of prompts.
3. **Normalization**: Hash the canonicalized payload `{prompt.strip(), model, temperature}` as sorted JSON — ensures `"hello "` and `"hello"` map to the same key.
4. **Security**: Raw prompts as keys could leak sensitive data in logs or monitoring dashboards.

---

### Q2: How does the LRU Cache achieve O(1) get and put?

**Answer:**
- **HashMap** provides O(1) key → node lookup.
- **Doubly Linked List** maintains access order — most recent at head, least recent at tail.
- **get**: lookup node in map → move to front → O(1).
- **put**: if exists, update + move to front. If new + at capacity, remove `tail.prev` (LRU) from both list and map, insert new node at front → O(1).
- **Sentinel nodes** (dummy head + tail) eliminate null checks on boundary operations.

---

### Q3: What is the difference between TTL-based and capacity-based cache eviction?

**Answer:**
| Strategy | Evicts When | Best For |
|----------|------------|---------|
| TTL | Entry age exceeds threshold | Time-sensitive data (weather, prices) |
| LRU | Least recently accessed when full | General-purpose, access-pattern driven |
| LFU | Least frequently accessed when full | Repeated popular queries |
| Semantic | Cosine similarity > threshold | Near-duplicate LLM prompts |

- **LLM caching best practice**: Combine TTL (stale response prevention) + LRU eviction (memory bound) + semantic deduplication (catch paraphrased prompts).

---

### Q4: How do you estimate cost savings from LLM caching?

**Answer:**
```
tokens_saved = cache_hits x avg_tokens_per_request
cost_saved   = tokens_saved / 1_000_000 x cost_per_1M_tokens

Example (Groq LLaMA3-8B @ $0.05/1M tokens):
  1000 cache hits x 350 tokens = 350,000 tokens saved
  cost_saved = 350,000 / 1,000,000 x 0.05 = $0.0175

At scale (1M requests/day, 40% hit rate):
  400,000 x 350 / 1M x 0.05 = $7/day = $2,555/year saved
```

---

### Q5: What is the LRU Cache DP/DSA connection to real systems?

**Answer:**
- LRU Cache (LC 146) is the exact data structure used in:
  - **CPU L1/L2 cache** page replacement
  - **Redis** with `maxmemory-policy allkeys-lru`
  - **Browser cache** for HTTP responses
  - **LLM semantic cache** for repeated prompt responses
- The HashMap + DLL pattern is the canonical O(1) solution — LinkedHashMap in Java provides this built-in via `accessOrder=true`.
