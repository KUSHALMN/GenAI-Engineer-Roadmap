# 🎯 Technical Interview Questions — Day 04: Multi-Tenancy & Structural Patterns

### 1. Compare the 3 Multi-Tenant Database Architectures: Shared Database + Shared Schema vs. Shared Database + Separate Schemas vs. Separate Databases.
**Answer:**
1. **Shared Database, Shared Schema (Tenant ID column):** Lowest compute/storage cost, easiest migrations, but highest risk of cross-tenant data leakage if a developer forgets a `WHERE tenant_id = ?` clause.
2. **Shared Database, Separate Schemas (Postgres Namespaces):** Better logical isolation, distinct table indexes, but schema migrations must run across thousands of schemas.
3. **Separate Database per Tenant:** Maximum security and compliance (HIPAA, PCI-DSS), easy point-in-time restores per customer, but high connection pool and resource overhead.

### 2. How does the Decorator Pattern simplify adding distributed tracing without modifying business logic?
**Answer:**
By wrapping service interfaces with a decorator that handles OpenTelemetry span creation, trace context injection, and error recording, core business handlers remain completely decoupled from observability SDKs.
