# 📝 Notes — Day 05: PostgreSQL Indexing & Exception Boundaries

## 1. PostgreSQL Indexing Strategies
- **Compound B-Tree:** Column order matters! An index on `(tenant_id, created_at)` satisfies queries on `tenant_id` and `(tenant_id, created_at)`, but NOT on `created_at` alone.
- **Partial Indexes:** Create indexes on subsets of rows (`WHERE is_active = true`) to save memory and write overhead.
