"""RAG Comparison: Benchmarking Dense vs BM25 vs Hybrid Search."""
import sys
import os

# Ensure Day-02 root is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from advanced_rag.hybrid_search import HybridSearchEngine
from advanced_rag.reranker import CrossEncoderReranker
from advanced_rag.citation_generator import CitationGenerator


def run_rag_comparison():
    docs = [
        {"id": "doc1", "title": "Vector Indexing", "content": "HNSW (Hierarchical Navigable Small World) provides logarithmic nearest neighbor graph search."},
        {"id": "doc2", "title": "Lexical Retrieval", "content": "BM25 scoring leverages term frequency and inverse document frequency to rank sparse tokens."},
        {"id": "doc3", "title": "Hybrid Fusion", "content": "Reciprocal Rank Fusion fuses ranks across lexical BM25 and dense embeddings without calibration."}
    ]

    engine = HybridSearchEngine(docs)
    query = "How does HNSW graph search work in vector databases?"

    # 1. Hybrid Search
    hybrid_results = engine.search(query, top_n=2)

    # 2. Rerank
    reranker = CrossEncoderReranker()
    reranked = reranker.rerank(query, hybrid_results, top_n=1)

    # 3. Citation
    output = CitationGenerator.generate_cited_answer(
        "HNSW builds a multi-layer graph hierarchy where greedy searches converge in logarithmic time.",
        reranked
    )

    print("=== ADVANCED RAG PIPELINE EXECUTION ===")
    print("Query   :", query)
    print("Top Hit :", reranked[0]["title"], f"(Score: {reranked[0]['rerank_score']})")
    print("Answer  :", output["answer_with_citations"])
    print("Sources :", output["citations"])


if __name__ == "__main__":
    run_rag_comparison()
