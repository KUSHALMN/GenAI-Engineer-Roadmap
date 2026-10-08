# 📅 Day 08 Notes — API Security & Number of Islands

## 🧠 What I Learned
1. **API Security Layers:**
   - Token Bucket rate limiter provides smooth burst handling while strictly enforcing requests-per-second constraints.
   - HMAC payload signatures prevent tampering across asynchronous agent queues and webhooks.
   - Canary token traps detect system prompt extractions at runtime with zero false positives.
2. **Connected Components on 2D Grids:**
   - 4-directional graph exploration: each cell $(r, c)$ connects to up to 4 neighbors.
   - In-place grid sinking eliminates the need for separate $\mathcal{O}(M \times N)$ visited storage.
   - Max Area of Island uses DFS return accumulation ($1 + \sum \text{dfs(neighbors)}$).
