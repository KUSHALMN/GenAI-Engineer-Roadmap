# 📅 Day 28: RAG Ablation Experiments & Interval DP

## 🎯 Deliverables
- **AI Engine**: `AI/ablation_runner.py`
  - Automated parameter ablation suite across chunk sizes, hybrid weights, top-K, and reranking.
  - Latency vs. Recall@K vs. MRR Pareto frontier analysis.
  - Reproducible CSV report persistence (`ablation_results.csv`).
- **Java DSA**: `DSA/IntervalDP.java`
  - LeetCode 312: Burst Balloons using Interval Dynamic Programming $\mathcal{O}(N^3)$.
  - Subproblem decoupling via "last balloon burst" state transition.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Ablation Runner
python Month-03/Day-28/AI/ablation_runner.py

# Java DSA
javac Month-03/Day-28/DSA/IntervalDP.java
java -cp Month-03/Day-28 DSA.IntervalDP
```
