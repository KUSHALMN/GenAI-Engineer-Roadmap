# Notes: Major Project 3: Production RAG v2 Release & Failure Analysis

## 1. Production Architecture Summary
Production RAG v2 unites all modules developed across Month 03 into a resilient, observable enterprise search service:
- **Ingestion**: Structure-aware parsing, incremental SHA-256 chunk hashing, multi-tenant ACL tagging.
- **Retrieval**: Dense vector embeddings + BM25 sparse keyword indices unified via Reciprocal Rank Fusion ($k=60$).
- **Precision Reranking**: Cross-encoder scoring of Top-50 candidates down to Top-5.
- **Context Optimization**: Contextual compression stripping irrelevant sentences while preserving citation source IDs.
- **Security**: Pre-retrieval role-based and tenant isolation gates.
- **Evaluation**: Continuous automated benchmark runner measuring Recall@K, MRR, NDCG@K, and citation grounding.

## 2. Failure Mode & Effects Analysis (FMEA)
| Failure Mode | Root Cause | Mitigation Implemented |
| :--- | :--- | :--- |
| **Hallucination under No Evidence** | Model attempts to answer when relevant docs don't exist | Unanswerable query calibration & strict abstention prompt rules |
| **Stale Search Results** | Document edited in storage but cached in vector store | Two-phase cascade deletion & index version cache invalidation |
| **Cross-Tenant Data Leak** | Post-filtering dropped results after retrieval | Hard SQL/payload pre-filtering before distance scoring |
