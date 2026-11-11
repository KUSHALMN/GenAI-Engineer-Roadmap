# 🎯 Technical Interview Questions — Day 19: Uncertainty Abstention & Trie Data Structures

## Question 1: How can an LLM system determine when to abstain ("I do not know") versus answering confidently?
**Answer:**
Production systems employ two complementary uncertainty estimation methods:
1. **White-box Logprob / Perplexity Analysis:** Inspect the normalized log-likelihood $\frac{1}{N} \sum \log P(w_i | w_{<i})$. Sequences with high perplexity indicate token-level uncertainty.
2. **Black-box Semantic Entropy:** Sample $K$ responses at temperature $T > 0$. Group answers into semantic equivalence clusters using bidirectional entailment. If the Shannon entropy $H = -\sum p_k \log p_k$ exceeds a calibrated threshold, the model has high epistemic uncertainty and should abstain with a polite refusal.
3. **Calibrated Abstention Trade-off:** By plotting the Coverage vs. Risk curve, teams calibrate thresholds so accuracy on answered questions exceeds 99% while abstaining on the hazardous long-tail.

---

## Question 2: Compare Trie search time and space complexity against a Hash Table for prefix lookups.
**Answer:**
- **Time Complexity:**
  - Trie lookup is $O(L)$ where $L$ is the length of the query string, completely independent of the total number of keys $N$.
  - Hash Table exact lookup is average $O(L)$ (computing the hash takes $O(L)$), but prefix queries (`startsWith`) require scanning all $N$ keys ($O(N \cdot L)$).
- **Space Complexity:**
  - Trie uses $O(\Sigma \cdot N \cdot L)$ where $\Sigma$ is the alphabet size (26 for lowercase English). Tries can share common prefixes, significantly compacting memory for large dictionaries.
  - A compressed Trie (Radix Tree) coalesces single-child chains, achieving near-optimal memory footprints.
