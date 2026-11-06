# Day 01: Technical Interview Preparation — Agent Architecture & Tool Contracts

### Q1: Compare deterministic workflows, ReAct agents, and Planner-Executor architectures.
**Answer:**
- **Deterministic Workflows (DAGs):** Fixed transitions; high reliability, predictable latency, zero hallucination of steps. Ideal for well-defined business logic (e.g., ETL, KYC forms).
- **ReAct (Reasoning + Acting):** Dynamic interleaving of thought, action, and observation. Highest flexibility for exploratory tasks where subsequent steps depend strictly on intermediate tool outputs, but can suffer from infinite loops and higher token cost.
- **Planner-Executor:** Upfront task decomposition into discrete subtasks followed by sequential/parallel execution. Offers high visibility and plan inspectability, but requires replanning capabilities when environment state violates initial assumptions.

### Q2: Why are typed tool contracts and explicit side-effect declarations critical for production LLM agents?
**Answer:**
1. **Schema Adherence:** LLMs generate JSON text. Strict typing (OpenAPI/JSON Schema) catches missing parameters and invalid types before reaching backend APIs.
2. **Safety & Permission Gating:** Marking `has_side_effects: true` (e.g., deleting a database record, sending an email) allows interceptors to mandate human approval or token authorization, whereas read-only tools can execute autonomously.
3. **Idempotency:** Tagging `is_idempotent: true` enables safe automatic retries on transient network failures without risking duplicate real-world operations.
