# 📝 Notes — Day 26: Model Deprecations & LRU Cache

- **Shadow Traffic Isolation:** Dark launch traffic must be executed asynchronously on background workers to avoid adding latency to the primary user path.
- **LRU Sentinel Nodes:** Use dummy `head` and `tail` nodes to eliminate boundary null-checks during insertion and removal.
