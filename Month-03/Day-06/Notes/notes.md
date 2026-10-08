# 📅 Day 06 Notes — LLM Guardrails & Lowest Common Ancestor

## 🧠 What I Learned
1. **Safety Layer Defense-in-Depth:**
   - Heuristic regex filters provide high-speed $O(1)$ rejection of known jailbreaks.
   - PII masking ensures compliance (GDPR/HIPAA) before sending data to 3rd-party LLM providers.
   - Output alignment computes grounding token overlap against context docs to reject ungrounded hallucinations.
2. **Lowest Common Ancestor Invariants:**
   - BST LCA utilizes key ordering: split point where $(p.val - curr.val) \times (q.val - curr.val) \le 0$.
   - General Binary Tree LCA uses post-order divide-and-conquer where both subtrees bubble up non-null markers.
