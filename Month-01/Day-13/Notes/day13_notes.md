# Day 13 Notes — Dockerized RAG + Hard Stack DSA

## AI — Dockerized Modular RAG Chatbot

### Package Structure (app/)
Each file has a single responsibility:
- `config.py` → all settings
- `loader.py` → PDF text extraction
- `splitter.py` → chunk with overlap
- `embedding.py` → lazy-loaded SentenceTransformer
- `vector_store.py` → ChromaDB upsert + query
- `retriever.py` → store chunks + retrieve top-k
- `prompt_builder.py` → format context + question
- `rag_pipeline.py` → ingest + query orchestrator
- `source_handler.py` → load + chunk in one call
- `main.py` → entry point

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "app.main"]
```

### Testing with pytest
```bash
pytest tests/
```
Tests run without LLM or DB — pure unit tests on splitter and prompt builder.

## DSA — Hard Stack Problem

### Largest Rectangle in Histogram — LeetCode #84
- Monotonic **increasing** stack of indices
- On pop: height = heights[popped], width = i - stack.peek() - 1
- Append virtual bar of height 0 to flush remaining stack
- Time: O(n), Space: O(n)

### Pattern Summary
| Problem | Stack Type | Trigger to Pop |
|---------|-----------|----------------|
| Daily Temperatures | Decreasing | current > top |
| Largest Rectangle | Increasing | current < top |
| Valid Parentheses | N/A | closing bracket |

## Key Takeaway
Monotonic stacks solve "next greater/smaller" and "largest area" problems in O(n). The direction (increasing vs decreasing) depends on what you're looking for.
