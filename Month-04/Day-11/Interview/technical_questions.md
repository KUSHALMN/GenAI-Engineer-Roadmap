# Day 11: Technical Interview Preparation — Agent Memory & 0/1 Knapsack

### Q1: What are the three core tiers of agent memory and how are they stored?
**Answer:**
1. **Working Memory (Scratchpad):** In-memory ephemeral buffer tracking thoughts and observations within the current turn. Discarded after task termination.
2. **Episodic Memory:** Chronological session chat messages. Stored in document stores (MongoDB/PostgreSQL). Compaction algorithms (sliding window, LLM summarization) keep it within token limits.
3. **Semantic Long-Term Memory:** Persistent user facts, preferences, and knowledge. Stored in vector databases (pgvector, Pinecone). Injected into prompts based on embedding similarity to current query.

### Q2: Why MUST the inner loop of 1D 0/1 Knapsack run in reverse (from `target` down to `num`)?
**Answer:**
If we iterate forwards from `num` to `target`, the updated value `dp[w - num]` computed in the *current* item iteration would be reused to update `dp[w]`, allowing the same item to be included multiple times (unbounded knapsack). Iterating backwards ensures `dp[w - num]` represents the state from the *previous* item iteration.
