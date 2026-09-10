# Day 12 Notes — Advanced RAG + Stack DSA

## AI — PDF RAG Chatbot (Advanced)

### Key Concepts
- **source_handler.py** — handles multiple input sources (PDF, URL, text)
- **retriever.py** — semantic search with ChromaDB
- **prompt_builder.py** — builds context-aware prompts
- **rag_pipeline.py** — orchestrates ingest → retrieve → answer
- **config.py** — single source of truth for all settings

### RAG Flow
```
Input Source → source_handler → chunks → ChromaDB
Query → retriever → top-k chunks → prompt_builder → LLM → Answer
```

## DSA — Stack Problems (Java)

### Valid Parentheses — LeetCode #20
- Use a stack, push open brackets, pop and match on close
- Time: O(n), Space: O(n)

### Daily Temperatures — LeetCode #739
- Monotonic decreasing stack storing indices
- Pop when current temp > stack top temp
- Time: O(n), Space: O(n)

### Evaluate Reverse Polish Notation — LeetCode #150
- Push numbers, pop two operands on operator
- Time: O(n), Space: O(n)

## Key Takeaway
Stack = LIFO. Perfect for matching pairs, next greater element, and expression evaluation.
