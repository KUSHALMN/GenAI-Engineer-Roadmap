# 📅 Month 03 — Advanced RAG & Search Engineering

> Topics: Production RAG v2, Hybrid Dense-Sparse Search, BM25, Reciprocal Rank Fusion (RRF), Query Rewriting, Multi-Query Retrieval, HyDE, Cross-Encoder Rerankers, Contextual Compression, Metadata Pre-Filtering, Citations & Source Attribution, Multi-Hop RAG, GraphRAG, Incremental Indexing, Vector Deletion Consistency, Permission-Aware Access Control (ACLs), Multilingual Embeddings, Query Routing, Retrieval Caching, IR Metrics (MRR, MAP, NDCG@K), Ablation Experiments, and Production FastAPI Services.

---

## 🎯 Day-by-Day Implementation Plan (Day 01 – Day 31)

| Day | GenAI / Search Engineering Topic | Key Deliverables (Python in `AI/`) | DSA (Java in `DSA/`) | Status |
|:---:|:---------------------------------|:-----------------------------------|:---------------------|:------:|
| [Day 01](Day-01/) | Context Engineering & Multi-Tier Memory | `conversation_memory.py`, `token_budget.py`, `summarizer.py`, `context_manager.py` | Disjoint Set Union & Kruskal MST (`DisjointSetMST.java`) | ✅ Done |
| [Day 02](Day-02/) | Advanced RAG & Multi-Stage Retrieval | `hybrid_search.py`, `bm25.py`, `hyde.py`, `reranker.py`, `parent_child_retrieval.py` | Advanced Backtracking LC 51, 79, 46 (`BacktrackingAdvanced.java`) | ✅ Done |
| [Day 03](Day-03/) | Multimodal GenAI Systems | `ocr_pipeline.py`, `audio_to_text.py`, `text_to_speech.py`, `image_qa.py`, `multimodal_rag.py` | Tree DP & Knapsack LC 337, 416, 322 (`TreeKnapsackDP.java`) | ✅ Done |
| [Day 04](Day-04/) | Hybrid Dense-Sparse Retrieval | `hybrid_dense_sparse_engine.py` (BM25 + Dense + RRF) | Tree BFS & Level Order LC 102, 103, 199 (`BinaryTreeLevelOrder.java`) | ✅ Done |
| [Day 05](Day-05/) | Cross-Encoder Rerankers & Compression | `cross_encoder_reranker.py` (Pairwise cross-attention) | Validate & Recover BST LC 98, 99 (`ValidateBST.java`) | ✅ Done |
| [Day 06](Day-06/) | Enterprise LLM Guardrails | `llm_guardrails_engine.py` (Prompt injection, PII masking) | Lowest Common Ancestor LC 235, 236 (`LowestCommonAncestorBST.java`) | ✅ Done |
| [Day 07](Day-07/) | Real-Time SSE Token Streaming | `streaming_token_pipeline.py` (W3C SSE chunks, backpressure) | Kth Smallest in BST LC 230 Morris & Stack (`KthSmallestBST.java`) | ✅ Done |
| [Day 08](Day-08/) | Production API Security & Defense | `api_security_suite.py` (Token bucket, HMAC-SHA256, Canary) | Number of Islands LC 200, 695 DFS/BFS (`NumberOfIslands.java`) | ✅ Done |
| [Day 09](Day-09/) | Hybrid Search with Reciprocal Rank Fusion | `hybrid_search_engine.py` (BM25 + Dense + RRF k=60) | LeetCode 295: Find Median from Data Stream (`MedianFinder.java`) | ✅ Done |
| [Day 10](Day-10/) | Conversational Query Rewriting | `query_rewriter.py` (Coreference, acronym expansion) | LeetCode 621: Task Scheduler & LC 767 (`TaskScheduler.java`) | ✅ Done |
| [Day 11](Day-11/) | Multi-Query Retrieval & Deduplication | `multi_query_retriever.py` (Subqueries, hash deduplication) | Disjoint Set Union: Connected Components LC 323 (`DisjointSetUnion.java`) | ✅ Done |
| [Day 12](Day-12/) | HyDE (Hypothetical Document Embeddings) | `hyde_retriever.py` (Zero-shot hypothetical hypothesis) | LeetCode 743: Network Delay Time Dijkstra (`DijkstraShortestPath.java`) | ✅ Done |
| [Day 13](Day-13/) | Cross-Encoder Candidate Reranking | `reranker_pipeline.py` (Bi-encoder recall + Cross-encoder precision) | Bellman-Ford Shortest Path & LC 787 Flights (`BellmanFord.java`) | ✅ Done |
| [Day 14](Day-14/) | Contextual Sentence Compression | `context_compressor.py` (Sentence prune, metadata preservation) | Floyd-Warshall All-Pairs Shortest Path O(V^3) (`FloydWarshall.java`) | ✅ Done |
| [Day 15](Day-15/) | Multi-Tenant Hybrid Pre-Filtering | `filtered_hybrid_retriever.py` (Tenant boundaries, RBAC) | Kruskal's Minimum Spanning Tree & LC 1584 (`KruskalMST.java`) | ✅ Done |
| [Day 16](Day-16/) | Citations & Source Attribution | `citation_engine.py` (Grounding audit, hallucinated cite traps) | Prim's Minimum Spanning Tree with Min-Heap (`PrimMST.java`) | ✅ Done |
| [Day 17](Day-17/) | Multi-Hop RAG & Decomposed Joins | `multi_hop_rag.py` (Sequential subqueries, provenance chains) | LeetCode 210: Course Schedule II Kahn's BFS (`TopologicalSort.java`) | ✅ Done |
| [Day 18](Day-18/) | GraphRAG Knowledge Graph Foundations | `build_graph.py` (Entity-relation triples, canonicalization) | Tarjan's Strongly Connected Components O(V+E) (`StronglyConnectedComponents.java`) | ✅ Done |
| [Day 19](Day-19/) | Graph Retrieval vs. Vector Search | `graph_retriever.py` (Multi-hop graph paths vs dense vector) | LeetCode 785: Is Graph Bipartite 2-Coloring (`BipartiteGraph.java`) | ✅ Done |
| [Day 20](Day-20/) | Incremental Indexing & Content Hash | `incremental_indexer.py` (SHA-256 chunk hashes, state-machine) | LeetCode 297: Serialize & Deserialize Binary Tree (`TreeSerialization.java`) | ✅ Done |
| [Day 21](Day-21/) | Document Deletion & Index Consistency | `delete_document_pipeline.py` (Tombstones, cascade purge) | LeetCode 236: Lowest Common Ancestor in Binary Tree (`LowestCommonAncestor.java`) | ✅ Done |
| [Day 22](Day-22/) | Permission-Aware RAG & Document ACLs | `acl_retriever.py` (Hard pre-filtering, negative security tests) | Self-Balancing AVL Binary Search Tree (`AVLTree.java`) | ✅ Done |
| [Day 23](Day-23/) | Multilingual & Cross-Lingual Search | `multilingual_search.py` (Language identification, BGE-M3 concept align) | Binary Indexed Tree / Fenwick Tree LC 307 (`FenwickTree.java`) | ✅ Done |
| [Day 24](Day-24/) | Dynamic Query Routing & Dispatch | `query_router.py` (Direct LLM, BM25, Text-to-SQL, Graph, Dense) | Segment Tree Range Sum Query O(log N) (`SegmentTree.java`) | ✅ Done |
| [Day 25](Day-25/) | Multi-Tier Retrieval & Embedding Cache | `retrieval_cache.py` (Canonical SHA-256 keys, TTL, index bump invalidation) | Sparse Table Range Minimum Query O(1) (`SparseTableRMQ.java`) | ✅ Done |
| [Day 26](Day-26/) | Golden Retrieval Evaluation Dataset | `retrieval_dataset_validator.py`, `retrieval_dataset.jsonl` | Bit Manipulation: Single Number I, II, III (`BitManipulationPatterns.java`) | ✅ Done |
| [Day 27](Day-27/) | Information Retrieval (IR) Metrics | `retrieval_metrics.py` (Precision@K, Recall@K, MRR, MAP, NDCG@K) | Bitmask Dynamic Programming: Optimal Assignment (`BitmaskDP.java`) | ✅ Done |
| [Day 28](Day-28/) | RAG Ablation Experiment Runner | `ablation_runner.py`, `ablation_results.csv` (Chunk size, hybrid weights) | LeetCode 312: Burst Balloons Interval DP O(N^3) (`IntervalDP.java`) | ✅ Done |
| [Day 29](Day-29/) | Production RAG FastAPI Integration | `rag_api_service.py` (REST endpoints: /health, /ingest, /query, /feedback) | Mixed Advanced DSA Suite: Trie, Graph, DP (`MixedAdvancedDSASet.java`) | ✅ Done |
| [Day 30](Day-30/) | Production RAG v2 Release & Audit | `rag_v2_audit_release.py` (FMEA report, regression audit) | 90-Min Capstone DSA Mock: LRU, Course Schedule, Heap (`ComprehensiveDSAMock.java`) | ✅ Done |
| [Day 31](Day-31/) | Enterprise RAG Benchmark Capstone | `enterprise_rag_benchmark.py` (End-to-end multi-stage pipeline) | Final DSA Mastery Capstone: Two-Heaps, Range Tree (`DSAMasteryCapstone.java`) | ✅ Done |

---

## 🏗️ Directory Architecture

Every day module strictly adheres to the established repository standard:
- `AI/` — **Python GenAI engines, retrieval algorithms, pipelines, and evaluation runners.**
- `DSA/` — **Runnable Java solutions with comprehensive `main` verification test drivers.**
- `Interview/` — **Technical Q&A deep-dives covering systems design and algorithm invariants.**
- `Notes/` — **Architecture notes, formulas, and theoretical design documentation.**
- `README.md` — **Daily deliverable summary, complexity analysis, and execution commands.**
