# Day 10 Notes — GenAI Engineer Roadmap

## Topics Learned

### Chain Architecture in RAG
New module `chain.py` introduced as the LLM execution layer:

| Module | Responsibility |
|--------|---------------|
| `loader.py` | Extract text from PDF |
| `splitter.py` | Word, sentence, paragraph splitting |
| `embedding.py` | Lazy model loading + encode |
| `vector_store.py` | ChromaDB add + search |
| `retriever.py` | Retrieve chunks with scores |
| `prompt_builder.py` | Build labeled context prompt |
| `chain.py` | LLM execution → returns question + context + answer |
| `rag_pipeline.py` | Orchestrate ingest + query |
| `app.py` | Thin entry point |

### New Concepts
- **chain.py** — dedicated LLM call layer, returns full result dict
- **Paragraph splitting** — splits at `\n\n`, preserves document structure
- **`query_with_context()`** — returns answer + context for debugging

---

## DSA (Java)

### Valid Parentheses — LeetCode #20
- Approach: Stack O(n)
- Push opening brackets, pop and match on closing brackets
- Return `stack.isEmpty()` at end

### Min Stack — LeetCode #155
- Approach: Two Stacks O(1) all operations
- Main stack stores all values
- Min stack only pushes when value ≤ current min
- `getMin()` = peek min stack

---

## Key Takeaway
The Stack data structure is perfect for problems that require tracking the most recent state — brackets, undo operations, min/max tracking. `chain.py` makes the LLM layer independently testable and swappable.
