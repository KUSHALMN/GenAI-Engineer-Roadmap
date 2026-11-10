# 📝 Notes — Day 04: Multi-Tenancy Data Design & Structural Patterns

## 1. Vector Search Isolation
- In Qdrant/Pinecone/Milvus, tenant filtering can be performed via payload filters or metadata namespaces.
- Separate namespaces avoid the "noisy neighbor" vector index rebalancing issue.

## 2. Row-Level Security (RLS)
- PostgreSQL native RLS (`ALTER TABLE docs ENABLE ROW LEVEL SECURITY`) automatically enforces `WHERE tenant_id = current_setting('app.current_tenant')` at the database engine layer.
