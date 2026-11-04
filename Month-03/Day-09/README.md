# 📅 Day 09: Hybrid Search Engine & Streaming Median

## 🎯 Deliverables
- **AI Engine**: `AI/hybrid_search_engine.py`
  - Robertson-Spärck Jones BM25 probabilistic term scoring ($k_1=1.5, b=0.75$).
  - Dense cosine similarity retriever.
  - Reciprocal Rank Fusion (RRF with $k=60$).
  - Min-max normalized linear score fusion.
- **Java DSA**: `DSA/MedianFinder.java`
  - LeetCode 295: Find Median from Data Stream with Two Balanced Heaps.
  - Insertion $\mathcal{O}(\log N)$, Median lookup $\mathcal{O}(1)$.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Hybrid Search
python Month-03/Day-09/AI/hybrid_search_engine.py

# Java DSA
javac Month-03/Day-09/DSA/MedianFinder.java
java -cp Month-03/Day-09 DSA.MedianFinder
```
