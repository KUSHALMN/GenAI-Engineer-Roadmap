# Day 27: Technical Interview Preparation — Regression Suites & KMP

### Q1: How do you eliminate flakiness when testing LLM-based agent systems in CI/CD?
**Answer:**
1. **Mock Tool Execution:** Replace actual external APIs with deterministic fixture mocks.
2. **Seed & Temperature Zero:** Force `temperature=0.0` and fixed seeds.
3. **Assert on Trajectory Constraints:** Test assertions against typed schema outputs and tool call sequences rather than exact natural language phrasing.

### Q2: What is the significance of the LPS (Longest Prefix Suffix) array in KMP?
**Answer:**
`lps[j]` stores the length of the longest proper prefix of `pattern[0..j]` that is also a suffix. When a mismatch occurs after matching $j$ characters, we know `pattern[0..lps[j-1]-1]` matches the text up to the mismatch point, allowing the algorithm to slide the pattern without ever decrementing the text index $i$.
