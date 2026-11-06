# Day 12: Technical Interview Preparation — Budget Policies & Coin Change

### Q1: How do you protect multi-tenant agent platforms against runaway model costs?
**Answer:**
1. **Hierarchical Quotas:** Set organization, project, and session level hard budgets for tokens and currency spend.
2. **Pre-Flight Estimation:** Estimate worst-case token cost before calling LLMs; reject requests if user wallet balance < threshold.
3. **Loop Detection Circuit Breaker:** Hash recent state/action tuples. If the agent repeats identical calls, terminate execution and return a descriptive warning.

### Q2: Compare Coin Change (Minimum Coins) with Combination Sum.
**Answer:**
- **Coin Change:** Seeks the *minimum count* of elements; solved efficiently using Dynamic Programming in $O(amount \times coins)$ time.
- **Combination Sum:** Seeks *all actual combinations*; requires backtracking tree exploration and is inherently exponential in the worst case.
