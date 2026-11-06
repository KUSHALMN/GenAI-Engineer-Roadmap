# Day 02: Technical Interview Preparation — Reliable Tool Dispatchers

### Q1: How do you prevent an agent tool from crashing the host process during execution?
**Answer:**
1. **Try-Except Wrapping with Structured Return:** Wrap the execution in a top-level dispatcher that catches base `Exception` and returns a structured response `{success: false, error: "..."}` rather than bubbling up unhandled exceptions.
2. **Process / Sandbox Isolation:** For high-risk or arbitrary code execution (e.g. Python REPL, shell commands), execute tools inside ephemeral subprocesses, containers, or WebAssembly runtimes with CPU/memory limits.
3. **Execution Timeouts:** Use `concurrent.futures` or async timeout shields so hanging network calls or infinite loops terminate cleanly.

### Q2: Why is sorting essential when generating subsets with duplicates?
**Answer:**
Sorting brings duplicate values together. During backtracking at recursion level `k`, if we have already branched on element `nums[i-1]`, branching on an identical element `nums[i]` (when `i > start`) generates an identical subtree. Sorting allows an O(1) adjacent duplicate check `nums[i] == nums[i-1]`.
