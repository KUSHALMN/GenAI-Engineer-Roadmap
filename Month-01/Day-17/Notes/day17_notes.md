# 📝 Day 17 Study Notes: Advanced RAG, Hybrid Search & Evaluation

---

## 1. Advanced Retrieval Paradigms

### Dense vs. Sparse Retrieval
| Dimension | Sparse Retrieval (BM25 / TF-IDF) | Dense Retrieval (Vector Embeddings) |
|---|---|---|
| **Mechanism** | Exact keyword matching & term frequency | Semantic concept proximity via cosine similarity |
| **Strengths** | Exact acronyms, part numbers, code names, rare tokens | Paraphrasing, synonyms, multi-lingual queries |
| **Weaknesses** | Vocabulary mismatch, misses context | Poor at exact ID / keyword lookup, domain shifts |

---

## 2. Hybrid Search & Reciprocal Rank Fusion (RRF)

Hybrid Search combines the best of dense vector search and sparse keyword retrieval.

### Reciprocal Rank Fusion (RRF) Formula
$$RRF(d) = \sum_{m \in M} \frac{w_m}{k + \text{rank}_m(d)}$$
Where:
- $k$ is a smoothing constant (typically $60$) to balance high ranks and dampen deep ranks.
- $w_m$ is an optional weight assigned to retriever $m$.
- $\text{rank}_m(d)$ is the 1-based position of document $d$ in system $m$.

---

## 3. Two-Stage Retrieval: Bi-Encoder vs. Cross-Encoder

1. **Stage 1 (Retrieval - Bi-Encoder):**
   - Independent embeddings computed for documents and queries in advance.
   - Extremely fast nearest neighbor lookup ($O(\log N)$ or fast matrix multiply).
   - Generates top $K$ (e.g., $K=20-50$) candidate passages.

2. **Stage 2 (Reranking - Cross-Encoder):**
   - Passes `(Query, Passage)` simultaneously through full multi-head transformer self-attention.
   - Computes deep cross-token interaction scores.
   - Prunes candidates down to top $k$ (e.g., $k=3-5$) with maximal precision.

---

## 4. The RAG Triad Evaluation Framework

1. **Context Relevance / Precision:** Is the retrieved passage relevant to the user query?
2. **Groundedness / Faithfulness:** Is the generated answer strictly backed by the context (no hallucination)?
3. **Answer Relevance:** Does the response directly address the user's inquiry?

### Key Metrics
- **MRR (Mean Reciprocal Rank):** Average reciprocal rank of first relevant item $\frac{1}{Q} \sum \frac{1}{\text{rank}_i}$.
- **Recall@K:** $\frac{\text{Relevant in top } K}{\text{Total Relevant}}$.
- **NDCG@K:** Normalized discounted cumulative gain rewarding relevant items ranked higher.
