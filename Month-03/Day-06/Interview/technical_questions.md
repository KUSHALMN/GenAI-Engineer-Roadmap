# 💬 Day 06: LLM Guardrails & Lowest Common Ancestor Interview Questions

### Q1: What constitutes a dual-rail guardrail architecture in enterprise GenAI?
**Answer:**
A dual-rail architecture inserts deterministic policy checks at two boundaries:
1. **Input Rails:** Inspect incoming user prompts prior to calling the LLM. They filter prompt injection attacks, jailbreaks (DAN, persona hijacking), PII (SSN, credit cards, emails), and out-of-scope domain requests.
2. **Output Rails:** Inspect the LLM's generated response prior to returning it to the user or downstream systems. They evaluate hallucination/grounding against retrieved passages, toxicity, tone, and schema compliance.

---

### Q2: How does the BST property simplify LCA compared to a general binary tree?
**Answer:**
In a BST, keys are ordered. We can determine which subtree contains the targets in $\mathcal{O}(1)$ time at each node:
- If both $p < \text{curr}$ and $q < \text{curr}$, LCA must be in the left subtree.
- If both $p > \text{curr}$ and $q > \text{curr}$, LCA must be in the right subtree.
- Otherwise, the paths to $p$ and $q$ diverge at $\text{curr}$, meaning $\text{curr}$ is the split point and the LCA.
This allows an iterative search with $\mathcal{O}(H)$ time and $\mathcal{O}(1)$ space, compared to general binary tree post-order recursion which requires $\mathcal{O}(N)$ time and $\mathcal{O}(H)$ call stack space.
