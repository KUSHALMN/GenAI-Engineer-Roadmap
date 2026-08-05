# Technical Questions — Day 10

## Chain Architecture

**Q: What is `chain.py` and why is it separate from `rag_pipeline.py`?**
> `chain.py` handles the LLM execution step — retrieve → prompt → call LLM → return result. `rag_pipeline.py` is the orchestrator that handles the full flow including ingestion. Separating them means you can swap the LLM provider without touching the pipeline logic.

**Q: What does `query_with_context()` return?**
> A dict with `question`, `context` (list of chunks), and `answer`. Useful for debugging retrieval quality — you can see exactly what context the LLM used to generate the answer.

**Q: What is paragraph splitting and when is it better than word splitting?**
> Paragraph splitting splits text at double newlines (`\n\n`). Better when the document has natural paragraph breaks — preserves semantic units. Word splitting is better for dense text without clear structure.

---

## Stack DSA

**Q: Why use a Stack for Valid Parentheses?**
> Brackets must be closed in LIFO order — the last opened bracket must be the first closed. Stack naturally models this behavior.

**Q: How does Min Stack work in O(1)?**
> Uses two stacks — one for all values, one tracking minimums. The min stack only pushes when a new value is ≤ current min. `getMin()` just peeks the min stack — O(1).

**Q: What is the difference between Stack and Queue?**
> Stack = LIFO (Last In First Out). Queue = FIFO (First In First Out). Stack uses `push/pop`, Queue uses `enqueue/dequeue`.

---

## Python

**Q: What is the difference between `split_by_words`, `split_by_sentences`, `split_by_paragraphs`?**
> Words: fixed size with overlap — good for dense text. Sentences: natural language boundaries — good for Q&A. Paragraphs: document structure boundaries — good for structured docs like reports.
