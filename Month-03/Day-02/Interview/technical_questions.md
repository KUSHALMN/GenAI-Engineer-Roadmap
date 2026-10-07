# 🎯 Day 02 (Month 03) Technical Interview Questions & Answers

## 1. Why does Hybrid Search with Reciprocal Rank Fusion (RRF) outperform purely Dense Vector Search?
**Answer:**
- **Dense Vector Search (Bi-Encoders)** maps semantics to high-dimensional geometry. It excels at fuzzy synonym matching (e.g., matching "automobile trouble" with "car engine breakdown"). However, it struggles with exact part numbers, acronyms, code identifiers, and rare proper nouns (out-of-vocabulary tokens).
- **Sparse BM25 Search** indexes exact lexical term frequency and inverse document frequency, excelling at exact identifier retrieval.
- **Reciprocal Rank Fusion (RRF)**:
  $$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
  RRF relies purely on relative ranking positions rather than raw uncalibrated similarity scores. It achieves the best of both worlds with zero hyperparameter fine-tuning.

---

## 2. What is HyDE (Hypothetical Document Embeddings), and when should you avoid using it?
**Answer:**
HyDE prompts an LLM to hallucinate a plausible hypothetical document that would answer the user's question, and uses the embedding of this *answer* to search the vector database rather than embedding the short user *question*.
- **When it shines**: Asymmetric retrieval where user queries are concise, ambiguous, or conceptually distant from the formal language in reference documents.
- **When to avoid**: Highly technical domains requiring strict factual accuracy (medical dosages, legal compliance numbers). The LLM may hallucinate false facts in the hypothetical document, biasing the vector search toward completely incorrect chunks.

---

## 3. How do you optimize N-Queens backtracking from $O(N!)$ to run in milliseconds?
**Answer:**
Instead of checking the entire row, column, and diagonal on every placement with an $O(N)$ loop, maintain three lookup hash sets or bitmasks:
1. `cols`: tracks occupied column indices.
2. `diag1`: tracks major diagonals ($row - col$).
3. `diag2`: tracks minor diagonals ($row + col$).
This reduces the validity check for any candidate position $(row, col)$ from $O(N)$ to $O(1)$ constant time, drastically cutting tree pruning overhead.
