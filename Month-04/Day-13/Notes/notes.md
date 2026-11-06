# Day 13 Notes: Agent Failure Recovery

## 1. Failure Taxonomy
- **Transient (Network/503):** Exponential backoff retry.
- **Contract/Schema (400):** Reflection & argument repair prompt.
- **Fatal (Auth/404):** Fallback tool or graceful degradation.
