# Notes: HyDE (Hypothetical Document Embeddings)

## 1. What is HyDE?
Hypothetical Document Embeddings (Gao et al., 2022) eliminates the query-document asymmetry in dense vector retrieval:
- **The Problem**: A user query ("How does backprop work?") is short, interrogative, and lacks document-style explanations. Corpus documents are long, assertive, and detail-rich.
- **The Solution**: An instruction-tuned LLM generates a speculative answer (even if factually hallucinated in fine details).
- **Why it Works**: The embedding of the hypothetical answer captures the *format, tone, domain terminology, and semantic structure* of the target document, shifting the query vector much closer to relevant answers in latent space.

## 2. Limitations and Caveats
1. **Hallucination Bias**: If the LLM generates completely false entities (e.g., invented library names), the search vector will drift toward irrelevant noise.
2. **Latency Penalty**: Requires an LLM inference call prior to vector index querying (adding ~300ms–1s).
3. **When to Avoid**: Exact code snippet lookups, part numbers, or queries where the model has zero pretraining knowledge.
