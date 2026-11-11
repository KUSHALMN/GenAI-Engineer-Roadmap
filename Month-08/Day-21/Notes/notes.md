# 📝 Notes — Day 21: Cost Observability & Java Collections

- **Token Economics:** Output tokens are typically 3x more expensive than prompt tokens due to auto-regressive KV cache generation.
- **Java Collection Allocations:** Prefer primitive specialized collections (Trove, fastutil) or pre-sized `ArrayList(initialCapacity)` to prevent repeated array reallocations and arraycopy costs.
