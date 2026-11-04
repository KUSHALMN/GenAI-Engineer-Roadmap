# Interview Questions: Month 03 Capstone & Enterprise RAG

### Q1: How do you defend the design choices of Production RAG v2 in a Staff Engineer system design interview?
**Answer**:
1. **Hybrid Retrieval with RRF**: Explain why vector search alone drops 30% recall on alphanumeric IDs and acronyms, justifying BM25 and why RRF is robust against disparate score scales.
2. **Two-Stage Retrieval (Bi-Encoder + Cross-Encoder)**: Explain that while bi-encoders optimize $\mathcal{O}(1)$ latency during recall, cross-encoders eliminate semantic false positives at the cost of $+40$ms, satisfying both precision and latency SLOs.
3. **Hard Pre-Filtering for Multi-Tenancy**: Explain why post-filtering is an operational security failure (can return empty results or leak metadata), whereas pre-filtering at index traversal time guarantees complete tenant boundaries.

### Q2: What is the primary difference between offline evaluation and online evaluation in RAG?
**Answer**:
- **Offline Evaluation**: Measures retrieval metrics (Recall@K, MRR, NDCG) and generation quality (faithfulness, answer relevance) against fixed golden labeled datasets before releasing code or prompt changes.
- **Online Evaluation**: Tracks live production telemetry (user thumbs up/down, citation click-through rate, latency p95/p99, cache hit rates, cost per query) and samples live production conversations for LLM-as-a-judge scoring and drift detection.
