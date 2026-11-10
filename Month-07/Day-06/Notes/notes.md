# 📝 Notes — Day 06: Redis Application Patterns & Java NIO

## 1. Redis Caching Topologies
- **Cache-Aside (Lazy Loading):** App queries cache first; on miss, queries DB and populates cache.
- **Write-Through:** App writes to cache, which synchronously updates DB.
- **Write-Behind (Write-Back):** App writes to cache; asynchronous background worker flushes writes to DB in batches.
