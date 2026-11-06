# Day 10: Technical Interview Preparation — Parallel Tools & 2D Grid DP

### Q1: When is parallel tool calling safe for an LLM agent, and when must it be sequential?
**Answer:**
- **Parallel Safe:** Independent, read-only tools without side effects or mutual data dependencies (e.g. querying weather in Tokyo and Paris simultaneously, or searching Wikipedia and Google News concurrently).
- **Sequential Required:** Dependent operations (e.g. `create_invoice()` must complete and return `invoice_id` before `send_email(invoice_id)` can be invoked), or concurrent mutations to shared state.

### Q2: How does 1D space optimization in 2D Grid DP work?
**Answer:**
In `dp[r][c] = dp[r-1][c] + dp[r][c-1]`, calculating row `r` only depends on the row immediately above `r-1` and the cell to the left in the current row `c-1`. Thus, we can maintain a single 1D array `dp[c]`: prior to update it holds `dp[r-1][c]`, and adding `dp[c-1]` produces the new value in-place.
