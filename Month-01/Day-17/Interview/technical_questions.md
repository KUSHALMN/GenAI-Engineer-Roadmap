# 🎯 Technical Interview Questions — Day 17 (Advanced RAG & Retrieval)

### Q1: What is the vocabulary mismatch problem in vector databases, and how does hybrid search solve it?
**Answer:**
Vector embeddings compress sentences into dense coordinates. However, when users search for specific alphanumeric codes, legal clause identifiers, product IDs, or rare medical acronyms, embeddings often place them near semantically related terms rather than the exact token. Sparse search (BM25) excels at exact term frequencies. Hybrid search combines both dense and sparse indices via algorithms like Reciprocal Rank Fusion (RRF), ensuring exact token matches and high-level semantic meaning are both captured.

---

### Q2: Why can't we use a Cross-Encoder for the entire 1,000,000 document corpus?
**Answer:**
A Bi-Encoder encodes documents offline once into vector space, enabling sub-millisecond approximate nearest neighbor (ANN) search over millions of vectors. A Cross-Encoder requires passing the query concatenated with every single document through all transformer attention layers at runtime ($O(N)$ full forward passes). Running a cross-encoder over 1M documents would take minutes and require massive GPU clusters. Thus, we use a two-stage pipeline: Bi-Encoder retrieves top 20-50 candidates in <10ms, and Cross-Encoder reranks those top candidates in ~50ms.

---

### Q3: What is RAGAS and how does it evaluate RAG systems without human annotations?
**Answer:**
RAGAS (Retrieval Augmented Generation Assessment) is a framework that evaluates RAG pipelines using LLM-assisted metrics:
- **Faithfulness:** Uses an LLM to extract statements from the answer and verifies if each statement is entailed by the retrieved context.
- **Answer Relevance:** Asks an LLM to generate potential questions from the answer and computes semantic similarity with the original query.
- **Context Precision & Recall:** Assesses whether the ground truth context chunks are ranked at the top of the context window.
