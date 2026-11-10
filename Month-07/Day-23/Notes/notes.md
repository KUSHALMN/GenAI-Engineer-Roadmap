# 📝 Notes — Day 23: LLM Provider Abstraction & Testing Discipline

## 1. Normalized Response Schema
- Maintain a single unified return schema regardless of upstream model: `provider`, `model`, `text`, `prompt_tokens`, `completion_tokens`, `latency_ms`.
