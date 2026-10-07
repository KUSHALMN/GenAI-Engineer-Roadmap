# 📅 Day 02 — Month 03: Advanced RAG Architecture & Multi-Stage Retrieval

> Build an end-to-end Advanced RAG pipeline: Sparse BM25 Search, Dense Embedding Retrieval, Reciprocal Rank Fusion (RRF), Conversational Query Rewriting, Multi-Query Generation, Hypothetical Document Embeddings (HyDE), Cross-Encoder Rerankers, Metadata Filtering, Parent-Child Hierarchical Chunking, and Citation Grounding Generators. Master Advanced Backtracking algorithms (LC 51 N-Queens, LC 79 Word Search, LC 46 Permutations) in Java.

---

## 📁 Architecture Overview

```
Day-02/
├── AI/
│   ├── advanced_rag/
│   │   ├── hybrid_search.py          # BM25 + Dense fusion via RRF
│   │   ├── bm25.py                   # Okapi BM25 implementation
│   │   ├── query_rewriter.py         # Conversational disambiguator
│   │   ├── multi_query.py            # Multi-perspective sub-query generator
│   │   ├── hyde.py                   # Hypothetical document expander
│   │   ├── reranker.py               # Cross-encoder relevance reranker
│   │   ├── metadata_filter.py        # Predicate filtering engine
│   │   ├── parent_child_retrieval.py # Hierarchical child search / parent return
│   │   └── citation_generator.py     # Attribution and source anchors
│   └── evaluation/
│       └── rag_comparison.py         # End-to-end pipeline benchmark runner
├── Java/
│   └── BacktrackingAdvanced.java     # LC 51 + LC 79 + LC 46 (Java)
├── DSA/
│   └── BacktrackingAdvanced.java     # Alternate DSA reference
├── Interview/
│   └── technical_questions.md        # Advanced RAG & Backtracking Q&A
├── Notes/
│   ├── notes.md                      # Theoretical deep-dive
│   └── README.md                     # Day documentation copy
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Advanced RAG Pipeline (Python in `AI/`)
```bash
python Month-03/Day-02/AI/evaluation/rag_comparison.py
```

### 2. Compile & Run Java Backtracking Suite (in `Java/`)
```bash
cd Month-03/Day-02/Java
javac BacktrackingAdvanced.java && java BacktrackingAdvanced
```
