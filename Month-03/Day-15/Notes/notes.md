# Notes: Multi-Tenant Filtered Hybrid Search

## 1. Pre-Filtering vs. Post-Filtering
- **Post-Filtering (Search First, Filter Later)**:
  - Vector database retrieves top $K$ nearest neighbors across the entire index; application then drops results failing tenant/department filters.
  - **Severe Defect**: If tenant A only owns 1% of the corpus, retrieving Top 10 might return 0 documents for Tenant A (Recall Collapse).
- **Pre-Filtering (Filter First, Search Within Valid Partition)**:
  - Vector index prunes its search graph to only traverse nodes belonging to `tenant_id` and authorized departments.
  - Guarantees $100\%$ tenant isolation and returns full Top-$K$ authorized candidates.

## 2. Inverted Index Payload Filters
Modern vector engines (Qdrant, Milvus, pgvector, Pinecone) build inverted bitmap indices on metadata payloads (`tenant_id`, `department`, `created_at`) allowing $\mathcal{O}(1)$ bitmask intersection prior to HNSW vector exploration.
