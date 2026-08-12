# Day 14 Notes — Multi-Document RAG + Sliding Window DSA

## AI — Multi-Document RAG Chatbot

### What changed from Day 13?
- Removed `prompt_builder.py` — prompt built inline in `rag_pipeline.py`
- Added `sample_documents/` — ingest multiple PDFs at once
- `main.py` now loops over all PDFs in `sample_documents/`

### Multi-Document Ingestion
```python
for filename in os.listdir(DOCS_DIR):
    if filename.endswith(".pdf"):
        ingest(os.path.join(DOCS_DIR, filename))
```

### Key Design Decisions
- All chunks from all documents go into the same ChromaDB collection
- Retrieval is cross-document — best matching chunks win regardless of source
- chunk IDs use index — upsert prevents duplicates on re-run

## DSA — Sliding Window (Java)

### Pattern
- Fixed window: maintain size k, slide by adding right and removing left
- Variable window: expand right, shrink left when condition violated

### Problems
- Maximum Average Subarray I — LeetCode #643 (fixed window)
- Longest Substring Without Repeating Characters — LeetCode #3 (variable window)
- Minimum Size Subarray Sum — LeetCode #209 (variable window)

## Key Takeaway
Sliding window = O(n) replacement for O(n²) nested loops when dealing with contiguous subarrays/substrings.
