# 📝 Notes — Day 26: Production Agent Deployment & Ring Buffers

## 1. Agent Sandbox Security
- Enforce strict tool execution timeouts (e.g., 10s max per tool call).
- Restrict filesystem access to isolated scratch directories using Linux cgroups / Docker containers.
