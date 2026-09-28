# Day 35 Notes — Month 02, Day 04
## Topic: LLM Caching & Cost Optimization + LRU Cache DSA

---

## AI: LLM Caching

### Cache Key Design
```python
key = SHA256(json.dumps({
    "prompt": prompt.strip(),
    "model": model,
    "temperature": temperature
}, sort_keys=True))
```
- Strip whitespace + sort keys = deterministic key for same logical request
- SHA-256 = fixed 64-char key, collision-resistant, safe to log

### Cache Architecture
```
Request → normalize prompt → SHA256 key
        → cache.get(key)
            HIT  → return cached response (0ms, $0 cost)
            MISS → call LLM API → cache.set(key, response, ttl)
```

### Eviction Strategy
1. TTL expiry — remove stale entries on access
2. LRU eviction — remove least recently used when max_size reached
3. Combined = production-ready cache

### Cost Savings Formula
```
savings = cache_hits × avg_tokens × cost_per_token
```

---

## DSA: LRU Cache (LC 146)

### Data Structures
- `HashMap<key, Node>` — O(1) lookup
- `Doubly Linked List` — O(1) order maintenance
- Sentinel head + tail — no null checks

### Operations
| Op | Steps | Time |
|----|-------|------|
| get | map lookup → move to front | O(1) |
| put (exists) | update val → move to front | O(1) |
| put (new, full) | remove tail.prev → insert front | O(1) |

### Key Pattern
```java
head ↔ [MRU] ↔ ... ↔ [LRU] ↔ tail
```
Always insert at `head.next`, always evict `tail.prev`.
