# 📅 Day 13: Cross-Encoder Reranking & Bellman-Ford

## 🎯 Deliverables
- **AI Engine**: `AI/reranker_pipeline.py`
  - Two-stage retrieval: Bi-encoder recall candidate generation + Cross-encoder precision reranking.
  - Pairwise cross-token coverage and bigram joint attention scoring.
  - Top-N truncation and score calibration.
- **Java DSA**: `DSA/BellmanFord.java`
  - Bellman-Ford single-source shortest path with negative edges $\mathcal{O}(V \times E)$.
  - Negative weight cycle detection on $V$-th iteration.
  - LeetCode 787: Cheapest Flights Within K Stops.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Cross-Encoder Pipeline
python Month-03/Day-13/AI/reranker_pipeline.py

# Java DSA
javac Month-03/Day-13/DSA/BellmanFord.java
java -cp Month-03/Day-13 DSA.BellmanFord
```
