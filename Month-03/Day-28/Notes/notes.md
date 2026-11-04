# Notes: RAG Ablation Experimentation Methodology

## 1. Single-Variable Controlled Experiments
In retrieval tuning, engineers frequently make the mistake of simultaneously changing the embedding model, increasing chunk size, adding BM25, and modifying prompt templates in one commit.
- **Result**: Impossible to determine which change contributed to improvement or caused regressions.
- **Ablation Discipline**: Hold all components constant while altering exactly one hyperparameter.

## 2. Key Ablation Variables
1. **Chunk Size (256 vs 512 vs 1024 tokens)**:
   - Smaller chunks: High precision, lower noise, but risk fragmenting long complex definitions.
   - Larger chunks: Preserves narrative context, but dilutes vector embeddings with tangential details.
2. **Dense vs Sparse Weight ($\alpha$)**:
   - $\alpha=1.0$: Pure vector search (misses exact product codes and rare acronyms).
   - $\alpha=0.0$: Pure BM25 (misses semantic synonyms and paraphrases).
   - $\alpha=0.6$: Hybrid sweet-spot for most enterprise corpora.
3. **Cross-Encoder Reranking**:
   - Trading $+45$ ms of latency for $+15$–$20\%$ boost in MRR and NDCG.
