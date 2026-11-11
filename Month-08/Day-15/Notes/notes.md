# 📝 Notes — Day 15: Prompt Injection Defenses & Backtracking

## 1. Multi-Layered Defense In Depth
- Layer 1: Regex / keyword heuristic blocklist.
- Layer 2: XML boundary containment.
- Layer 3: Secondary classifier LLM verifying output safety before streaming to user.
