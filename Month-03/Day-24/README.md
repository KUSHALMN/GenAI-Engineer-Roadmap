# 📅 Day 24: Query Routing & Segment Trees

## 🎯 Deliverables
- **AI Engine**: `AI/query_router.py`
  - Multi-path semantic query classifier and intent detector.
  - Specialized dispatch to Direct LLM, Text-to-SQL, BM25, GraphRAG, and Vector HNSW.
  - Estimated latency profiling and reasoning audit trails.
- **Java DSA**: `DSA/SegmentTree.java`
  - Array-based Segment Tree implementation with $\mathcal{O}(N)$ build.
  - Point update $\mathcal{O}(\log N)$ and Range Sum Query $\mathcal{O}(\log N)$.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Query Router
python Month-03/Day-24/AI/query_router.py

# Java DSA
javac Month-03/Day-24/DSA/SegmentTree.java
java -cp Month-03/Day-24/DSA SegmentTree
```
