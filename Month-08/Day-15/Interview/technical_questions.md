# 🎯 Technical Interview Questions — Day 15: Injection Defenses & Backtracking

### 1. What is the "Instruction Hierarchy" architectural defense against prompt injection?
**Answer:**
Instruction hierarchy enforces structural privilege levels in foundation models:
1. **System Instructions (Tier 1 - Highest Authority):** Set by application developers; cannot be overridden.
2. **Context / Ingested RAG Chunks (Tier 2 - Data Only):** Treated strictly as read-only evidence. If context contains text like "System: do X", the model ignores it as unprivileged data.
3. **User Query (Tier 3 - Untrusted Input):** Wrapped in explicit tags (`<user_input>`) and restricted from issuing control directives.

### 2. What is the difference between Subsets, Permutations, and Combinations in Backtracking?
**Answer:**
- **Subsets ($2^N$):** Every subset size from $0$ to $N$; order does not matter. The recursive step advances `start + 1`.
- **Combinations ($\binom{N}{K}$):** Subsets of a strictly fixed size $K$.
- **Permutations ($N!$):** Order matters (`[1, 2]` is distinct from `[2, 1]`). The loop iterates from $0$ to $N$ with a `visited` array or list removal.
