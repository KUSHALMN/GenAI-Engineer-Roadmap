# 📅 Day 35 — Month 02, Day 04: LLM Caching & Cost Optimization + LRU Cache

> Build a production LLM response cache with SHA-256 keying, TTL expiry, and cost tracking. Master LRU Cache (LC 146) with O(1) HashMap + Doubly Linked List in Java.

---

## 📁 Structure

```
Day-04/
├── src/
│   ├── llm_cache.py      # In-memory cache — SHA-256 keys, TTL, LRU eviction, stats
│   └── cached_llm.py     # Groq LLM wrapper with cache + cost savings tracker
├── tests/
│   └── test_llm_cache.py # 10 unit tests — TTL, keying, eviction, hit rate
├── DSA/
│   └── LRUCache.java     # LC 146 — O(1) get/put via HashMap + DLL (Java)
├── Interview/
│   └── technical_questions.md  # SHA-256 keying, LRU O(1), TTL vs LRU, cost math
└── Notes/
    └── notes.md
```

---

## 🧠 AI: LLM Cache

### Run Tests
```bash
cd Month-02/Day-04
pytest tests/test_llm_cache.py -v
```

### Run Cached LLM (needs GROQ_API_KEY)
```bash
export GROQ_API_KEY=your_key
python src/cached_llm.py
```

### Cache Key Design
```python
SHA256(json.dumps({"prompt": prompt.strip(), "model": model, "temperature": t}, sort_keys=True))
```

### Stats Output
```
[API]   What is RAG in AI?... (342ms)
[CACHE] What is RAG in AI?... (0ms)
[API]   Explain LoRA fine-tuning... (289ms)
[CACHE] What is RAG in AI?... (0ms)

Stats: {size: 2, hits: 2, misses: 2, hit_rate: 0.5, tokens_saved: 700, cost_saved_usd: 0.000035}
```

---

## ☕ DSA: LRU Cache — LC 146 (Java)

**Pattern**: HashMap + Doubly Linked List — O(1) get & put

```
head ↔ [MRU] ↔ ... ↔ [LRU] ↔ tail
```

### Run
```bash
cd Month-02/Day-04/DSA
javac LRUCache.java
java LRUCache
```

**Expected output:**
```
1
-1
-1
3
4
```

---

## 🎯 Key Takeaways

1. **SHA-256 keying** with prompt normalization prevents spurious cache misses from whitespace differences.
2. **TTL + LRU combined** = production cache — TTL prevents stale responses, LRU bounds memory.
3. **LRU Cache O(1)** requires both HashMap (lookup) and DLL (order) — neither alone is sufficient.
4. **Sentinel nodes** in DLL eliminate edge-case null checks on head/tail operations.

---

## ✅ Status: Done
