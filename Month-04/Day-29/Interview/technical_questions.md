# Day 29: Technical Interview Preparation — E2E Testing & Wildcard Matching

### Q1: What are the primary failure modes in End-to-End MCP Agent integration?
**Answer:**
1. **Schema Mismatch:** Model outputs arguments with string integers (e.g. `"100"`) when the server expects a float number.
2. **Deadlocks in stdio Buffering:** Large payloads exceed the OS pipe buffer size without being flushed, causing client and server to block indefinitely.
3. **Authentication Token Expiry:** Long-running multi-turn tool workflows fail midway because the caller's bearer token expires before final tool invocation.

### Q2: In Wildcard Matching DP, why does `dp[i-1][j]` represent `*` matching one or more characters?
**Answer:**
`dp[i-1][j]` checks if the prefix `s[0..i-2]` matched the pattern `p[0..j-1]`. If true, the `*` at `p[j-1]` can simply absorb the current character `s[i-1]` as well, extending its sequence match without consuming the `*`.
