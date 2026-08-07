# Day 11 Notes — GenAI Engineer Roadmap

## Topics Learned

### Config-Driven Architecture
Introduced `config.py` as single source of truth:

```python
# config.py
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL    = "llama-3.3-70b-versatile"
CHUNK_SIZE   = 200
OVERLAP      = 30
COLLECTION_NAME = "pdf_rag"
N_RESULTS    = 3
PDF_PATH     = "sample.pdf"
```

All modules now import from config — no hardcoded values anywhere.

### Benefits of config.py
- Change model in one place → affects entire pipeline
- Easy to create dev/prod configs
- No magic strings scattered across files

---

## DSA (Java)

### Implement Queue using Stacks — LeetCode #232
- Approach: Two Stacks, amortized O(1)
- `inbox` receives pushes, `outbox` serves pops/peeks
- Transfer only when outbox is empty

### Number of Recent Calls — LeetCode #933
- Approach: Queue sliding window O(1) amortized
- Add ping to queue, remove all pings older than `t - 3000`
- Queue size = number of recent calls

---

## Key Takeaway
Config-driven code is production-ready code. Queue = FIFO — perfect for sliding window problems and task scheduling. Stack = LIFO — perfect for bracket matching and undo operations.
