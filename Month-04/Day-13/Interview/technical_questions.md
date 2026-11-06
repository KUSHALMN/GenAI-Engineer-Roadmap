# Day 13: Technical Interview Preparation — Agent Recovery & LIS

### Q1: How do you design self-reflection prompts when an agent encounters an unrecoverable tool error?
**Answer:**
1. **Structured Failure Injection:** Append the exact error message and tool signature to the context.
2. **Reflection Instruction:** Prompt: "Tool `X` failed with error `Y`. Reflect on why this failure occurred. Did you provide invalid arguments or is the target resource missing? Do NOT repeat the exact same call. Choose an alternative tool or explain to the user what information is required."
3. **Negative Constraints:** Instruct the model never to fabricate results if a tool is permanently unreachable.

### Q2: Explain the intuition behind Patience Sorting in $O(n \log n)$ LIS.
**Answer:**
`tails[i]` stores the smallest tail element of all increasing subsequences of length `i + 1` found so far. For each number `x`, we binary search for the first element in `tails` $\ge x$. If found, we update that tail to `x` (giving future numbers a better chance to extend the subsequence). If `x` is larger than all current tails, we extend the subsequence length by 1.
