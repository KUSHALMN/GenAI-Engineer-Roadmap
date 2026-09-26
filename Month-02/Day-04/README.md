# 📅 Day 34 — Month 02, Day 04: LLM Caching & Cost Optimization

> Build an in-memory LLM response cache with TTL, deterministic cache-key generation, telemetry metrics, and a wrapper that adds transparent caching around an LLM API call. Implement an LRU Cache from scratch in Python and Java.

---

## 📁 Structure

```
Day-04/
├── llm_cache.py                # Deterministic SHA256 key gen + metrics (hits/misses/cost/latency saved)
├── ttl_cache.py                # Thread-safe in-memory cache with TTL expiration
├── cached_llm.py               # Transparent LLM wrapper with timing and cache bypass
├── lru_cache.py                # LRU Cache from scratch (DLL + HashMap) & FrequencyCounter
├── cost_optimization_notes.md  # Architectural notes on exact vs semantic caching & pricing formulas
├── README.md
└── DSA/
    ├── LRUCache.java           # LC 146 - LRU Cache in Java (O(1) get & put)
    └── FrequencyCounter.java   # HashMap frequency counting + Top-K min-heap in Java
```

---

## 🚀 Key Features Implemented

1. **Deterministic Hashing**: Canonical serialization of request messages, model, and sampling parameters via SHA-256.
2. **TTL In-Memory Expiration**: Thread-safe cache with background and on-access eviction for stale completions.
3. **Telemetry & Cost Tracking**: Tracks exact tokens saved, dollar cost saved based on provider rates, and latency speedups.
4. **LRU Cache from Scratch**: Implemented using custom Doubly Linked List nodes and Hash Map without `functools.lru_cache` or `OrderedDict`.

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python lru_cache.py
python ttl_cache.py
python llm_cache.py
python cached_llm.py
```

### Java Tests
```bash
cd DSA
javac LRUCache.java FrequencyCounter.java
java LRUCache
java FrequencyCounter
```

---

## ✅ Status: Completed
