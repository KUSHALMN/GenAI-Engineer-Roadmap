# 🎯 Day 27 Technical Interview Questions & Answers

## 1. What are the key architectural differences between Input Guardrails, Model System Prompts, and Output Guardrails?
**Answer:**
- **Input Guardrails (Pre-LLM)**: Run deterministically in microsecond/millisecond latency before the LLM is called. They perform token ceiling enforcement, regex & embedding-based PII redaction, topic classification, and prompt injection screening. Advantage: Saves LLM inference compute costs on malicious/toxic prompts.
- **Model System Prompts (In-LLM)**: Guide model behavior and tone using probabilistic natural language instructions. Disadvantage: Susceptible to jailbreaks and prompt leakage.
- **Output Guardrails (Post-LLM)**: Intercept LLM output before it reaches the client. They enforce JSON schema validation, hallucination grounding, check for unmasked API secrets/PII leaks, and verify tone/policy compliance.

---

## 2. Why is Human-In-The-Loop (HITL) mandatory for high-risk agentic tools?
**Answer:**
Agents equipped with tool execution capabilities can trigger irreversible external actions (e.g., executing SQL `DROP TABLE`, transferring bank funds, deleting AWS S3 buckets, sending emails to customers).
Because LLMs are non-deterministic and subject to hallucination or indirect prompt injection, high-risk tools cannot execute autonomously. A HITL gate halts workflow execution, emits a structured approval event to an operator dashboard or webhook, and awaits signed human confirmation before proceeding.

---

## 3. How do you serialize and deserialize a binary tree in $O(N)$ time with preorder traversal (LeetCode 297)?
**Answer:**
- **Serialization**: Perform a Preorder DFS (Root -> Left -> Right). If a node is null, append a sentinel marker (e.g. `"#,"`). If non-null, append `node.val + ","`. This yields a unique string representation including structural boundary information.
- **Deserialization**: Split the string by commas into a FIFO `Queue<String>`. Recursively poll the next token: if it's `"#"` return `null`. Otherwise, instantiate `TreeNode(val)` and recursively construct `.left` and `.right`. Because each node and null marker is visited once, both serialization and deserialization take strictly $O(N)$ time and $O(N)$ memory.
