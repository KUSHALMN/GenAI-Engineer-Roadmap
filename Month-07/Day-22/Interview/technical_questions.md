# 🎯 Technical Interview Questions — Day 22: Privacy & Circuit Breakers

### 1. What are the engineering requirements for GDPR "Right to be Forgotten" in a RAG system?
**Answer:**
1. **Relational Database Purging:** Remove all session records, audit rows, and user account metadata.
2. **Vector Database Deletion:** Must delete all vector points and chunks tagged with `user_id` or `tenant_id`.
3. **Model Weight Auditing:** Customer data must never be directly trained or baked into foundational model weights unless guaranteed unlearning procedures exist.
4. **Log & S3 Purging:** S3 files must be purged and logs anonymized.

### 2. Explain the state transitions of the Circuit Breaker pattern.
**Answer:**
- **CLOSED:** Normal operation; all requests pass to upstream provider. If error rate exceeds threshold within a rolling window, transitions to **OPEN**.
- **OPEN:** Fails fast immediately without calling the upstream service, returning a fallback response. After a sleep window (e.g., 30s), transitions to **HALF-OPEN**.
- **HALF-OPEN:** Allows a limited probe set of requests. If they succeed, resets to **CLOSED**; if any fail, returns to **OPEN**.
