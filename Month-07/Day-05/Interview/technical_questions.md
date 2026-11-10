# 🎯 Technical Interview Questions — Day 05: PostgreSQL Indexing & Exceptions

### 1. When should you use a GIN (Generalized Inverted Index) over a B-Tree index in PostgreSQL?
**Answer:**
- **B-Tree:** Best for single scalar values, range queries (`>`, `<`), equality checks, and sorting (`ORDER BY`).
- **GIN Index:** Best for composite or multi-valued data types like arrays, full-text search vectors (`tsvector`), and `JSONB` documents containing arbitrary key-value pairs or tags. GIN builds an internal inverted index where each item/element points to a list of matching tuple IDs (TIDs), drastically speeding up `@>` (jsonb contains) queries.

### 2. Why should unchecked exceptions be preferred over checked exceptions in modern layered architectures?
**Answer:**
Checked exceptions force intermediate architectural layers to declare `throws` or rewrap exceptions, violating encapsulation. Unchecked runtime exceptions cleanly propagate to top-level exception handlers (e.g., `@ControllerAdvice` or FastAPI error handlers) where consistent HTTP envelopes are synthesized.
