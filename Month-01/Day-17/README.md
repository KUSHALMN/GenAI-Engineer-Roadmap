# Month 1 - Day 17

## Topics Learned
- Advanced Retrieval: Dense Semantic vs. Sparse BM25
- Hybrid Search with Reciprocal Rank Fusion (RRF)
- Cross-Encoder Reranking for Precision Refinement
- End-to-End PDF RAG Chatbot Architecture
- RAG Evaluation Metrics (MRR, Recall@K, Precision@K, NDCG)
- DSA — Binary Trees & Binary Search Trees (Java)

## Python
- `bm25_retriever.py` — Okapi BM25 implementation from scratch
- `reciprocal_rank_fusion.py` — RRF algorithm for multi-retriever rank merging
- `eval_metrics.py` — Precision@K, Recall@K, MRR, NDCG calculation functions

## DSA (Java)
- `invert_binary_tree.java` — LeetCode #226 (Invert Binary Tree)
- `binary_tree_level_order.java` — LeetCode #102 (Level Order Traversal)
- `validate_bst.java` — LeetCode #98 (Validate Binary Search Tree)
- `kth_smallest_bst.java` — LeetCode #230 (Kth Smallest Element in a BST)

## AI Project: PDF RAG Chatbot
- Full modular project under `AI/pdf-rag-chatbot/` featuring:
  - Document loader (`app/loader.py`)
  - Recursive text splitter (`app/splitter.py`)
  - Semantic vector retriever (`retrieval/semantic_retriever.py`)
  - BM25 keyword retriever (`retrieval/keyword_retriever.py`)
  - Hybrid RRF retriever (`retrieval/hybrid_retriever.py`)
  - Cross-scoring reranker (`retrieval/reranker.py`)
  - Evaluation harness (`evaluation/evaluate.py`, `evaluation/questions.json`, `evaluation/results.json`)
  - FastAPI server (`app/main.py`)

## Interview Prep
- `technical_questions.md` — Bi-Encoders vs Cross-Encoders, RAGAS, Vocabulary mismatch
- `coding_questions.md` — BST validation, BFS level order, RRF in Python

---

## Folder Structure

```
Day-17/
├── Python/
│   ├── bm25_retriever.py
│   ├── reciprocal_rank_fusion.py
│   └── eval_metrics.py
├── DSA/
│   ├── invert_binary_tree.java
│   ├── binary_tree_level_order.java
│   ├── validate_bst.java
│   └── kth_smallest_bst.java
├── AI/
│   ├── README.md
│   └── pdf-rag-chatbot/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── loader.py
│       │   ├── splitter.py
│       │   ├── embedding.py
│       │   ├── vector_store.py
│       │   ├── prompt_builder.py
│       │   ├── source_handler.py
│       │   ├── rag_pipeline.py
│       │   └── main.py
│       ├── retrieval/
│       │   ├── __init__.py
│       │   ├── semantic_retriever.py
│       │   ├── keyword_retriever.py
│       │   ├── hybrid_retriever.py
│       │   └── reranker.py
│       ├── evaluation/
│       │   ├── questions.json
│       │   ├── evaluate.py
│       │   └── results.json
│       ├── tests/
│       │   ├── __init__.py
│       │   └── test_rag.py
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── .env.example
│       ├── .gitignore
│       └── README.md
├── Interview/
│   ├── technical_questions.md
│   └── coding_questions.md
├── Notes/
│   └── day17_notes.md
├── Resources.md
└── README.md
```

## How to Run

**Python Scripts:**
```bash
python Python/bm25_retriever.py
python Python/reciprocal_rank_fusion.py
python Python/eval_metrics.py
```

**DSA (Java):**
```bash
javac DSA/invert_binary_tree.java && java -cp DSA invert_binary_tree
javac DSA/binary_tree_level_order.java && java -cp DSA binary_tree_level_order
javac DSA/validate_bst.java && java -cp DSA validate_bst
javac DSA/kth_smallest_bst.java && java -cp DSA kth_smallest_bst
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
python -m app.main
python evaluation/evaluate.py
python -m unittest tests/test_rag.py
```
