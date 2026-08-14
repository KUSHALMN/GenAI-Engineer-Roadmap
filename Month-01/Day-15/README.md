# Month 1 - Day 15

## Topics Learned
- Hybrid Search RAG — semantic + keyword + hybrid retrieval
- Binary Tree DFS — inorder traversal, max depth
- Modular retrieval/ package with swappable strategies

## DSA (Java)
- Binary Tree Inorder Traversal — LeetCode #94
- Maximum Depth of Binary Tree — LeetCode #104

## AI Project
- PDF RAG Chatbot (Hybrid Search)
  - `app/` — core pipeline modules
  - `retrieval/semantic_retriever.py` — ChromaDB vector search
  - `retrieval/keyword_retriever.py` — keyword overlap scoring
  - `retrieval/hybrid_retriever.py` — merge + deduplicate both

## Interview Prep
- `technical_questions.md` — hybrid search, tree DFS
- `coding_questions.md` — Java & Python patterns
- `recruiter_questions.md` — project walkthrough

## What I Learned
Hybrid retrieval combines the strengths of semantic and keyword search. Tree DFS problems follow a consistent pattern: base case returns 0/null, recursive case combines left + right results.

---

## Folder Structure

```
Day-15/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app/
│       │   ├── main.py
│       │   ├── config.py
│       │   ├── loader.py
│       │   ├── splitter.py
│       │   ├── embedding.py
│       │   ├── vector_store.py
│       │   ├── retriever.py
│       │   ├── prompt_builder.py
│       │   ├── rag_pipeline.py
│       │   └── source_handler.py
│       ├── retrieval/
│       │   ├── semantic_retriever.py
│       │   ├── keyword_retriever.py
│       │   └── hybrid_retriever.py
│       ├── tests/
│       │   └── test_health.py
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── .env.example
│       ├── .gitignore
│       └── README.md
├── DSA/
│   ├── inorder_traversal.java
│   └── max_depth_binary_tree.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
├── Notes/
│   └── day15_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/inorder_traversal.java && java -cp DSA inorder_traversal
javac DSA/max_depth_binary_tree.java && java -cp DSA max_depth_binary_tree
```

**RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

**Tests:**
```bash
pytest tests/
```
