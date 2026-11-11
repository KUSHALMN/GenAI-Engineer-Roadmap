# 🎯 Technical Interview Questions — Day 09: Prompt Versioning & Trees

### 1. Why should prompts be treated as code with immutable versioning in Git/Registries?
**Answer:**
A prompt is an executable program for an LLM. Minor phrasing tweaks, comma changes, or whitespace adjustments can drastically alter model behavior, trigger regressions, or bypass safety guardrails. Storing prompts in versioned registries with SHA-256 hashes enables rollbacks, deterministic audit trails, and correlation with evaluation benchmark runs.

### 2. What is the maximum possible recursion depth when computing the depth of a binary tree?
**Answer:**
In a balanced binary tree, the call stack depth is $O(\log N)$. In a degenerate tree (resembling a singly linked list), the recursion depth is $O(N)$, which can trigger a `StackOverflowError` if the tree contains tens of thousands of skewed nodes.
