# 🎯 Day 29 Technical Interview Questions: Production RAG Optimization

### Q1: Why can't we use a Cross-Encoder for the entire database search instead of a Bi-Encoder?
**Answer**:
- **Bi-Encoder (Embedding Vector Search)**: Documents are pre-embedded and indexed into an HNSW or IVF index offline. At query time, we only embed the query ($O(1)$) and perform approximate nearest neighbor dot-product search ($O(\log N)$). It can search millions of documents in 10ms.
- **Cross-Encoder (Reranker)**: Feeds query and document jointly through all transformer self-attention layers ($O(L^2)$ attention complexity per document). Running a Cross-Encoder against 1,000,000 documents would take minutes or hours.
- *Solution*: A two-stage architecture: Bi-encoder filters 1,000,000 down to 50 candidates in 15ms; Cross-encoder reranks those 50 candidates down to the top 3 in 40ms.

---

### Q2: What metrics does RAGAS measure and how do they diagnose RAG failures?
**Answer**:
1. **Faithfulness**: Are claims in the generated answer grounded in the retrieved context? (Low score = Model hallucinated).
2. **Answer Relevance**: Does the generated answer address the user's initial question? (Low score = Model wandered or answered tangentially).
3. **Context Recall**: Did the retriever retrieve all chunks needed to answer the question? (Low score = Retrieval stage failure / poor chunking).
4. **Context Precision**: Are the ground-truth relevant chunks ranked near the very top of the retrieved set? (Low score = Need a better reranker).
