# Day 8 Notes — GenAI Engineer Roadmap

## Topics Learned

### Refactoring RAG Pipeline
- Split monolithic app into modular files
- **Single Responsibility Principle** — each file does one thing
- `embedding.py` — handles model loading and encoding
- `vector_store.py` — handles ChromaDB operations
- `chunking.py` — handles text splitting strategies
- `pdf_loader.py` — handles PDF extraction

### Lazy Loading Pattern
- Load heavy resources (ML models) only when first needed
- Use a global `_model = None` and check before loading
- Saves startup time and memory

### ChromaDB — `get_or_create_collection`
- Safe way to initialize collection
- Prevents errors when running the script multiple times

---

## DSA (Java)

### Binary Search — LeetCode #704
- Approach: Binary Search O(log n)
- `mid = left + (right - left) / 2` — avoids integer overflow
- Return -1 if not found

### Search Insert Position — LeetCode #35
- Same as binary search but return `left` when not found
- `left` naturally lands at the correct insert position

---

## Interview Prep
- Reviewed RAG architecture questions
- Practiced binary search coding problems
- Prepared HR answers: strengths, challenges, goals

---

## Key Takeaway
Good code is modular code. Splitting a working script into focused modules makes it easier to test, maintain, and scale — a critical skill for production AI engineering.
