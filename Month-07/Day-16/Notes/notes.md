# 📝 Notes — Day 16: Rate Limiting & Elevator System Design

## 1. Multi-Tenant Rate Limiting
- Return standard headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.
- Store quota counters in Redis with sliding-window Lua scripts for atomic updates across multi-pod deployments.
