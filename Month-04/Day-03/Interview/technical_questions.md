# Day 03: Technical Interview Preparation — Tool Routing and Selection

### Q1: When should you use a deterministic router vs LLM-based tool calling?
**Answer:**
- **Deterministic Keyword/Embedding Router:** Best when tool boundaries are distinct, latency must be sub-10ms, cost must be zero, or when strict regulatory policies prohibit sending raw prompts to third-party models prior to classification.
- **LLM Function Calling:** Best when user requests are syntactically complex, contain multiple chained operations, or require contextual parameter extraction simultaneously with tool selection.

### Q2: What is the computational complexity difference between subsets and permutations?
**Answer:**
- **Subsets (Power Set):** $2^n$ combinations. Each element has 2 choices (include/exclude). Total time is $O(n \cdot 2^n)$.
- **Permutations:** $n!$ combinations. The first slot has $n$ choices, second has $n-1$, etc. Total time is $O(n \cdot n!)$.
- Factorial growth ($n!$) grows far more rapidly than exponential ($2^n$).
