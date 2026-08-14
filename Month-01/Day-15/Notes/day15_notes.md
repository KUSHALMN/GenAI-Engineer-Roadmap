# Day 15 Notes — Hybrid Search RAG + Binary Tree DSA

## AI — Hybrid Search RAG

### Three Retrieval Strategies

**Semantic Retrieval** (`semantic_retriever.py`)
- Embeds query → ChromaDB vector similarity search
- Finds conceptually similar chunks even without exact word match
- Best for: "explain machine learning" → finds ML-related chunks

**Keyword Retrieval** (`keyword_retriever.py`)
- Splits query into keywords → counts overlap with each chunk
- Simple but effective for exact term matching
- Best for: "GROQ_API_KEY" → finds chunks with that exact term

**Hybrid Retrieval** (`hybrid_retriever.py`)
- Runs both, merges results, deduplicates, returns top-k
- Best overall — catches both semantic and exact matches

### Hybrid Merge Logic
```python
seen, merged = set(), []
for chunk in semantic + keyword:
    if chunk not in seen:
        seen.add(chunk)
        merged.append(chunk)
return merged[:TOP_K]
```
Semantic results take priority (listed first), keyword fills gaps.

## DSA — Binary Trees (Java)

### Key Concepts
- **Inorder** (Left → Root → Right) → sorted order for BST
- **Preorder** (Root → Left → Right) → copy/serialize tree
- **Postorder** (Left → Right → Root) → delete tree, evaluate expression

### Max Depth — LeetCode #104
```java
return Math.max(maxDepth(root.left), maxDepth(root.right)) + 1;
```

## Key Takeaway
Hybrid search > pure semantic search. Semantic catches meaning, keyword catches exact terms — together they cover more ground.
