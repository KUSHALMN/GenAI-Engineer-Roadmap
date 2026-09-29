# Day 21 (Month 02): Interview Questions
## Focus: LLM Evaluation, Metrics, Two Pointers DSA

---

### Q1: What is the RAG Triad and why does it matter for evaluation?

**Answer:**
The RAG Triad measures three dimensions of RAG quality:
1. **Context Relevance**: Is the retrieved context relevant to the question? Irrelevant context wastes tokens and confuses the LLM.
2. **Groundedness / Faithfulness**: Is the answer supported by the retrieved context? Detects hallucinations.
3. **Answer Relevance**: Does the answer actually address the question asked?

A response can be grounded but irrelevant, or relevant but hallucinated — all three must be measured independently.

---

### Q2: Why is Exact Match insufficient as a standalone LLM evaluation metric?

**Answer:**
- EM requires character-perfect match — penalizes valid paraphrases (`"RAG combines retrieval and generation"` vs `"RAG is retrieval-augmented generation"`).
- **Better pipeline**: EM → Token F1 → BERTScore → LLM-as-Judge, each adding semantic depth.
- EM is useful for structured outputs (SQL, JSON, code) where exact format matters.
- For open-ended generation, Token F1 + LLM Judge is the production standard.

---

### Q3: How do you prevent position bias in LLM-as-Judge evaluation?

**Answer:**
- Position bias: LLM judges tend to prefer the first response shown (primacy bias).
- **Fix**: Run each comparison twice with swapped order (A vs B, then B vs A). Only count as a win if the same response wins both times; otherwise mark as tie.
- Also use **calibration prompts** — known good/bad pairs to verify the judge is scoring correctly before running on real data.

---

### Q4: Two Pointers — when to use vs Sliding Window?

**Answer:**
| Pattern | Use When | Example |
|---------|----------|---------|
| Two Pointers | Sorted array, pair/triplet search, converging from ends | Two Sum II, 3Sum, Container Water |
| Sliding Window | Subarray/substring with constraint, contiguous elements | Longest substring, max sum subarray |

Key distinction: Two Pointers work from **both ends inward**; Sliding Window expands/contracts from **one end**.
