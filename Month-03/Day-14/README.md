# 📅 Day 14: Contextual Compression & Floyd-Warshall Algorithm

## 🎯 Deliverables
- **AI Engine**: `AI/context_compressor.py`
  - Sentence-level relevance filtering and semantic noise pruning.
  - Source ID, page number, and chunk metadata preservation.
  - Compression ratio metrics and zero-recall fallback safeguard.
- **Java DSA**: `DSA/FloydWarshall.java`
  - Floyd-Warshall all-pairs shortest paths $\mathcal{O}(V^3)$ DP.
  - Negative weight cycle detection via diagonal entry checking.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Contextual Compression
python Month-03/Day-14/AI/context_compressor.py

# Java DSA
javac Month-03/Day-14/DSA/FloydWarshall.java
java -cp Month-03/Day-14/DSA FloydWarshall
```
