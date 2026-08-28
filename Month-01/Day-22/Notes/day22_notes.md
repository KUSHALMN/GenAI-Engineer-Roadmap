# 📚 Day 22: Enterprise PDF RAG Chatbot, Hybrid Retrieval & Advanced Sliding Window

---

## 🎯 Daily Learning Objectives
1. **End-to-End PDF RAG Architecture**: Document loading (`pypdf`), recursive chunking with metadata, and semantic indexing.
2. **Hybrid Search & Fusion**: Combining Sparse Lexical BM25 with Dense Cosine Embeddings using Reciprocal Rank Fusion (RRF).
3. **Real-time SSE Token Streaming**: Building an async Server-Sent Events generator for typing effect and measuring TTFT.
4. **Containerization & Testing**: Creating production multi-stage Dockerfiles and comprehensive pytest suites.
5. **Algorithmic Mastery (Sliding Window in Java)**:
   - Longest Substring Without Repeating Characters (LeetCode 3)
   - Longest Repeating Character Replacement (LeetCode 424)
   - Minimum Window Substring (LeetCode 76 - Hard)

---

## 🧠 Core Architectural Concepts

### 1. Hybrid Retrieval and Reciprocal Rank Fusion (RRF)
Hybrid search overcomes the limitations of standalone dense vector search:
- **Dense Vector Search**: Excels at semantic meaning ("automobile" $\leftrightarrow$ "car") but struggles with exact model IDs, serial numbers, or code identifiers (e.g. `CVE-2024-38077`).
- **Sparse BM25 Search**: Matches exact keywords and rare terminology using Inverse Document Frequency.
- **RRF Integration**: Combines ranks without needing to calibrate arbitrary score distributions:
  $$\text{RRF}(d) = \sum_{m} \frac{w_m}{k + \text{rank}_m(d)}$$

---

### 2. SSE Streaming vs Polling
- **Server-Sent Events (SSE)** uses standard HTTP persistent connections with `text/event-stream` MIME type.
- Each event is formatted as:
  ```http
  data: {"type": "token", "content": "Hello"}

  data: {"type": "done", "latency_ms": 250.4}
  ```
- Dramatically improves perceived user responsiveness and reduces Time-To-First-Token (TTFT).

---

### 3. Java Sliding Window Paradigms

```
        Window [left ... right]
          ├── Expand: Increment right, update frequency counts.
          └── Shrink / Slide:
                ├── Variable Window: while (invalid) { shrink left }
                └── Fixed / Non-shrinking Window: if (invalid) { slide left++ }
```

1. **LeetCode 3**: Hash index map jumps `left = max(left, lastSeen[c] + 1)`.
2. **LeetCode 424**: Invariant `window_len - max_freq <= k`. Non-shrinking window optimization achieves $O(N)$ with zero inner while loops.
3. **LeetCode 76**: Track `have` vs `need` distinct character matches. Shrink from `left` once valid to find the minimum length window.

---

## 🛠️ Verification & Practical Exercises
- [x] Run Java test suites: `javac DSA/*.java && java DSA/...`
- [x] Run Python test suite: `pytest AI/pdf-rag-chatbot/tests/ -v`
- [x] Test streaming endpoint via curl / FastAPI Swagger docs
