# Notes: Hybrid Search Architecture & Reciprocal Rank Fusion (RRF)

## 1. Sparse vs. Dense Retrieval
- **Sparse (BM25)**:
  - Exact lexical keyword matching based on probabilistic TF-IDF term saturation ($k_1$) and document length normalization ($b$).
  - Excels at acronyms, part numbers, exact identifiers, rare entities, and specific jargon.
  - Vocabulary mismatch problem: fails when users use synonyms (e.g., "automobile" vs "car").
- **Dense Vector Search**:
  - Encodes semantic meaning in continuous dense space via dual-encoder models (e.g., MiniLM, BGE, Ada-002).
  - Captures contextual similarity, intent, and cross-lingual meaning.
  - Vulnerable to out-of-domain terms, rare alphanumeric IDs, and hallucinated relevance.

## 2. Fusion Strategies
### A. Reciprocal Rank Fusion (RRF)
$$\text{RRF}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
- Where $k$ is typically set to $60$.
- Advantage: Distribution-free; doesn't require calibrating disparate score scales between vector cosine similarities and unbounded BM25 scores.

### B. Min-Max Normalized Weighted Linear Combination
$$\text{Score}(d) = \alpha \cdot \hat{S}_{\text{dense}}(d) + (1 - \alpha) \cdot \hat{S}_{\text{bm25}}(d)$$
- Requires normalizing sparse and dense score distributions to $[0, 1]$ before convex weighting.
