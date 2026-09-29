# Day 22 (Month 02): Interview Questions
## Focus: Advanced RAG Evaluation, RAG Triad, Sliding Window DSA

---

### Q1: What is the RAG Triad and how do you measure each dimension?

**Answer:**
1. **Context Relevance** — Does the retrieved context contain information needed to answer the question?
   - Measure: keyword overlap between question tokens and context tokens.
   - LLM Judge: "Is this context relevant to the question? Score 1-5."

2. **Faithfulness** — Is every claim in the answer supported by the context?
   - Measure: token overlap between prediction and context.
   - LLM Judge: "Is this answer fully grounded in the context? Score 1-5."

3. **Answer Relevance** — Does the answer actually address the question?
   - Measure: token F1 between prediction and expected answer.
   - LLM Judge: "Does this answer address the question? Score 1-5."

---

### Q2: Why does Exact Match score 0.0 in the Day-22 report even though answers are correct?

**Answer:**
- The predictions are semantically correct paraphrases but not character-identical to expected answers.
- Example: Expected = `"Hybrid search combines dense vector search and BM25..."` vs Predicted = `"Hybrid search combines vector similarity search with BM25..."`.
- This is why EM alone is insufficient — Token F1 (0.78) and faithfulness (0.68) better reflect true quality.
- **Lesson**: Always use multiple metrics. EM is a lower bound; semantic metrics reveal true performance.

---

### Q3: Sliding Window — fixed vs variable size. When to use each?

**Answer:**
| Type | Window Size | Shrink Condition | Example |
|------|------------|-----------------|---------|
| Fixed | Constant k | Always slide by 1 | Find anagrams (LC 438), max avg subarray |
| Variable | Dynamic | When constraint violated | Min subarray sum (LC 209), longest substring (LC 3) |

- **Fixed**: iterate with `r - l + 1 == k` always true.
- **Variable**: expand `r`, shrink `l` while constraint is violated (sum >= target, duplicate char, etc.).

---

### Q4: How do you scale LLM-as-Judge evaluation cost-efficiently?

**Answer:**
1. **Sample-based evaluation**: Run LLM Judge on 10-20% random sample, not full dataset.
2. **Smaller judge model**: Use LLaMA3-8B instead of GPT-4 for bulk scoring — 10x cheaper.
3. **Cache judge results**: SHA-256 key on (question + context + prediction) — identical inputs reuse cached scores.
4. **Hybrid pipeline**: Use fast heuristics (Token F1, EM) to filter obvious failures first, only run LLM Judge on borderline cases.
5. **Batch API calls**: Group multiple samples in one prompt with structured JSON output for all samples at once.
