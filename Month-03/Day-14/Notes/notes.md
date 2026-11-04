# Notes: Contextual Compression & Chunk Pruning

## 1. Why Contextual Compression Matters
Retrieved chunks from raw documents (typically 500–1000 tokens each) often contain conversational noise, boilerplate disclaimers, or irrelevant paragraphs alongside the desired answer.
- **Lost in the Middle**: LLM attention degrades when relevant facts are buried in long context windows.
- **Token Cost**: Passing 10 full chunks (8,000 tokens) costs $4\times$ more than extracting only the 4 relevant sentences (500 tokens).
- **Hallucination Suppression**: Removing extraneous assertions prevents the LLM from hallucinating answers based on unrelated facts in the same chunk.

## 2. Invariants in Compression
1. **Source Attribution Preservation**: Every compressed passage must retain its `source_id`, `chunk_id`, and page metadata.
2. **Recall Fallback**: If no sentence clears the similarity threshold, keep the single highest-scoring sentence rather than discarding the chunk entirely to prevent zero-recall failures.
