# Day 9 Notes — GenAI Engineer Roadmap

## Topics Learned

### Full Modular RAG Pipeline
Built the most complete version of the RAG chatbot with 8 dedicated modules:

| Module | Responsibility |
|--------|---------------|
| `pdf_loader.py` | Extract text from PDF |
| `chunking.py` | Split text into word/sentence chunks |
| `embedding.py` | Lazy model loading + encode text |
| `vector_store.py` | ChromaDB add + search |
| `retriever.py` | Retrieve chunks with distance scores |
| `prompt_builder.py` | Build labeled context prompt |
| `rag_pipeline.py` | Orchestrate ingest + query |
| `app.py` | Thin entry point (10 lines) |

### New Concepts
- **retriever.py** — returns chunks with distance scores for quality evaluation
- **prompt_builder.py** — labels chunks [Chunk 1], [Chunk 2] for clearer LLM context
- **rag_pipeline.py** — single orchestrator, hides all complexity from app.py
- **Thin entry point** — app.py should be as small as possible

---

## DSA (Java)

### Valid Palindrome — LeetCode #125
- Approach: Two Pointers O(n)
- Skip non-alphanumeric chars with inner while loops
- Compare lowercased chars from both ends

### Merge Sorted Array — LeetCode #88
- Approach: Two Pointers from end O(m+n)
- Start from the back to avoid overwriting nums1 elements
- Fill from position `m+n-1` downward

---

## Key Takeaway
A production RAG system is not one script — it's a pipeline of focused modules. Each module should be independently testable and replaceable. Today's architecture is close to what you'd see in a real AI product.
