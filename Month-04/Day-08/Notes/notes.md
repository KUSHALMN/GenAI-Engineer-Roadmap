# Day 08 Notes: Agent Checkpoints and Resume

## 1. Checkpointing Patterns
- **Write-Ahead State:** Save state *before* invoking critical tools or *immediately after* receiving responses.
- **Storage Backends:** Ephemeral in-memory during testing; DynamoDB/PostgreSQL/Redis in production.
