# 📅 Day 15: Multi-Tenant Hybrid Filtering & Kruskal's MST

## 🎯 Deliverables
- **AI Engine**: `AI/filtered_hybrid_retriever.py`
  - Multi-tenant hard boundary enforcement (`tenant_id`).
  - Department and role-based access control (RBAC) payload filtering.
  - Date threshold validation and pre-filtering execution pipeline.
- **Java DSA**: `DSA/KruskalMST.java`
  - Kruskal's Minimum Spanning Tree with Edge Sorting and DSU $\mathcal{O}(E \log V)$.
  - Cycle detection using Disjoint Set Union with Rank and Path Compression.
- **Interview & Notes**:
  - `Interview/technical_questions.md`
  - `Notes/notes.md`

## 🚀 Execution & Verification
```bash
# Python Multi-Tenant Filtered Search
python Month-03/Day-15/AI/filtered_hybrid_retriever.py

# Java DSA
javac Month-03/Day-15/DSA/KruskalMST.java
java -cp Month-03/Day-15 DSA.KruskalMST
```
