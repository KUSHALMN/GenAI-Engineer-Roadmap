# 📅 Day 22: Enterprise PDF RAG Chatbot, SSE Streaming & Sliding Window DSA

Welcome to **Day 22** of the **GenAI Engineer Roadmap**! Today focuses on building a production-grade PDF RAG Chatbot with FastAPI, hybrid dense/sparse retrieval with Reciprocal Rank Fusion (RRF), real-time Server-Sent Events (SSE) streaming, and mastering Hard-level Sliding Window DSA problems in Java.

---

## 📁 Day 22 Project Structure

```
Day-22/
├── Notes/
│   └── day22_notes.md
│
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app/
│       │   ├── main.py              # FastAPI application & REST endpoints
│       │   ├── rag_pipeline.py      # End-to-end RAG orchestrator & citations
│       │   ├── streaming.py         # Async Server-Sent Events (SSE) token generator
│       │   └── config.py            # Environment & model configurations
│       │
│       ├── retrieval/
│       │   ├── __init__.py
│       │   ├── pdf_loader.py        # PDF page extractor with metadata
│       │   ├── chunking.py          # Recursive character text splitter
│       │   ├── vector_store.py      # Dense vector store with cosine search
│       │   └── hybrid_retriever.py  # BM25 + Dense RRF fusion retriever
│       │
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── test_rag.py          # Unit tests for chunking & retrieval
│       │   └── test_api.py          # API integration tests with TestClient
│       │
│       ├── requirements.txt
│       ├── Dockerfile
│       └── README.md
│
├── DSA/
│   ├── longest_substring.java       # LeetCode 3: Longest Substring Without Repeating
│   ├── character_replacement.java   # LeetCode 424: Longest Repeating Character Replacement
│   └── minimum_window_substring.java # LeetCode 76: Minimum Window Substring (Hard)
│
├── Interview/
│   ├── technical_questions.md       # RAG, Hybrid Search & SSE Streaming Q&A
│   ├── coding_questions.md          # Sliding Window algorithmic deep dives
│   └── recruiter_questions.md       # Behavioral & system design talking points
│
├── Resources.md
└── README.md
```

---

## ⚡ Highlights & Key Capabilities

1. **Hybrid Retrieval with Reciprocal Rank Fusion (RRF)**:
   - Fuses Okapi BM25 keyword matches with Dense Vector semantic embeddings.
2. **Server-Sent Events (SSE) Token Streaming**:
   - Real-time token streaming via `/api/v1/query/stream` with TTFT metrics.
3. **Verifiable Citations**:
   - Exact source, page number, and chunk references returned with every answer.
4. **Full Test Suite & Dockerization**:
   - Multi-stage non-root container and comprehensive automated pytest suite.
5. **Java Sliding Window Solutions**:
   - Multiple optimal implementations with exhaustive unit tests and complexity analysis.

---

## 🚀 Quick Execution Commands

### Run Python RAG Tests
```bash
pytest Month-01/Day-22/AI/pdf-rag-chatbot/tests/ -v
```

### Run Java DSA Solutions
```bash
javac Month-01/Day-22/DSA/*.java
java -cp Month-01/Day-22/DSA longest_substring
java -cp Month-01/Day-22/DSA character_replacement
java -cp Month-01/Day-22/DSA minimum_window_substring
```
