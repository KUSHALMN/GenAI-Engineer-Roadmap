# 🎯 Technical Interview Questions — Day 30: Project 7 Capstone Release

### 1. Walk through the end-to-end request lifecycle of a query in the Project 7 Platform.
**Answer:**
1. **Client / Gateway:** HTTPS request hits Cloudflare / AWS ALB for TLS termination and WAF filtering.
2. **Reverse Proxy & Auth:** Reverse proxy checks JWT signature, extracts `tenant_id` and roles, and verifies non-revocation in Redis.
3. **Rate Limiting:** Token bucket checks tenant quota. If exhausted, returns `429 Retry-After`.
4. **Router / Service:** Routes to Document Service with OpenTelemetry span creation (`traceparent`).
5. **Data Layer:** Row-level security restricts queries to `WHERE tenant_id = ?`.
6. **Async Tasks:** Heavy chunking/embedding is enqueued to Celery/Redis with idempotency keys.
7. **Response:** Sanitized JSON envelope returned to client.

### 2. How does a Trie structure optimize search suggestions over a relational database `LIKE 'prefix%'` query?
**Answer:**
A database `LIKE 'prefix%'` scan requires traversing a B-Tree index with disk I/O, which degrades under heavy concurrent autocomplete typing. A Trie resides in memory with $O(L)$ lookup time (where $L$ is prefix length), completely independent of the total number of words in the dictionary.
