# 📅 Day 44 — Month 02, Day 14: Advanced RAG

> Implement query rewriting (HyDE, decomposition, keyword expansion), hybrid retrieval fusing BM25 sparse and dense vector similarity via Reciprocal Rank Fusion (RRF), cross-encoder reranking, metadata filtering, citation-based generation, and a comparative evaluation of baseline vs advanced RAG. Implement Graph BFS/DFS, Connected Components, and Cycle Detection in Python and Java.

---

## 📁 Structure

```
Day-14/
├── query_rewriter.py       # HyDE, sub-query decomposition, and keyword expansion
├── hybrid_retriever.py     # BM25 + Dense vector retrieval fused via Reciprocal Rank Fusion (RRF)
├── reranker.py             # Second-stage cross-encoder contextual reranker
├── metadata_filter.py      # Pre- and post-filtering engine with comparison operators
├── citation_rag.py         # Response generator with inline citations & RAG comparison report
├── graph_bfs_dfs.py        # Graph BFS/DFS, Number of Islands (LC 200), Cycle Detection (LC 207)
├── README.md
└── DSA/
    └── GraphPatterns.java  # Graph BFS/DFS & Kahn's Cycle Detection in Java
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python query_rewriter.py
python hybrid_retriever.py
python reranker.py
python metadata_filter.py
python citation_rag.py
python graph_bfs_dfs.py
```

### Java Tests
```bash
cd DSA
javac GraphPatterns.java
java GraphPatterns
```

---

## ✅ Status: Completed
