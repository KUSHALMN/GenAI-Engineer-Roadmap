# 📅 Day 23 Notes: Corrective RAG (CRAG), Self-RAG & LRU Cache

---

## 🧠 Core Concepts

### 1. Corrective RAG (CRAG) Workflow
1. **Document Retrieval:** Dense / sparse retrieval returns candidate chunks.
2. **Retrieval Evaluator:** Evaluates semantic relevance scores.
   - Confidence $\ge \gamma_{high} \implies$ **Correct**
   - $\gamma_{low} \le$ Confidence $< \gamma_{high} \implies$ **Ambiguous**
   - Confidence $< \gamma_{low} \implies$ **Incorrect**
3. **Knowledge Refinement (Decomposition):** Breaks paragraphs into sentence-level strips and filters non-matching sentences to eliminate noise before LLM context packing.
4. **Web Search Fallback:** Rewrites query to broaden keyword coverage when documents fail evaluation.

### 2. Self-RAG (Self-Reflective RAG)
- Uses reflection tokens (`[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`) to gate generation.
- Enables autonomous self-correction loops when hallucinations are detected.

---

## ☕ DSA: LeetCode 146 — LRU Cache
- **Data Structures:** `HashMap<Integer, Node>` + Doubly Linked List with dummy `head` and `tail`.
- **Time Complexity:** $O(1)$ for both `get` and `put`.
- **Space Complexity:** $O(\text{capacity})$.
