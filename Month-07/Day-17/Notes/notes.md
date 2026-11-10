# 📝 Notes — Day 17: Load Balancing & Autoscaling

## 1. Load Balancing Algorithms for Inference
- **Least Connections / Least In-Flight:** Strongly preferred over Round-Robin because LLM response times vary drastically by output token length.
- **Session Affinity (Sticky Sessions):** Can be useful for multi-turn conversations leveraging prefix caching.
