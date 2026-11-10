# 🎯 Technical Interview Questions — Day 29: PRR & System Design Mock

### 1. What are the key categories in a standard Production Readiness Review (PRR)?
**Answer:**
1. **Design & Architecture:** Single points of failure, multi-AZ resilience, circuit breakers.
2. **Observability:** Golden signals (Latency, Traffic, Errors, Saturation), alerting burn rates, OpenTelemetry tracing.
3. **Security & Compliance:** Secrets rotation, RBAC, PII redaction, dependency CVE scans.
4. **Operations & Incident Response:** Runbooks, disaster recovery RPO/RTO drills, on-call schedules.

### 2. How do you scale a URL Shortener to handle 10,000 writes/second?
**Answer:**
Avoid database auto-increment bottlenecks by using distributed ID generation (e.g., Twitter Snowflake or Redis ranges allocated per worker pod). Cache hot URL redirections in Redis with an LRU eviction policy to handle read-heavy traffic (99% reads, 1% writes).
