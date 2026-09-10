from __future__ import annotations

import unittest
from app.loader import Document
from app.splitter import RecursiveCharacterTextSplitter
from app.vector_store import VectorStore
from retrieval.keyword_retriever import KeywordRetriever
from retrieval.semantic_retriever import SemanticRetriever
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from app.rag_pipeline import RAGPipeline


class TestRAGComponents(unittest.TestCase):

    def setUp(self):
        self.sample_docs = [
            Document(
                text="PostgreSQL is a powerful, open-source object-relational database system.",
                metadata={"source": "db_overview.pdf", "page": 1},
            ),
            Document(
                text="FastAPI is a modern, fast web framework for building APIs with Python 3.8+.",
                metadata={"source": "api_guide.pdf", "page": 1},
            ),
            Document(
                text="Retrieval-Augmented Generation (RAG) enhances LLM answers with relevant context retrieved from external documents.",
                metadata={"source": "rag_tutorial.pdf", "page": 2},
            ),
            Document(
                text="Hybrid search uses both BM25 keyword matching and vector embeddings with Reciprocal Rank Fusion.",
                metadata={"source": "hybrid_search.pdf", "page": 3},
            ),
        ]

    def test_text_splitter(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
        chunks = splitter.split_text("This is a long sentence that should be partitioned into several smaller overlapping chunks of text.")
        self.assertGreater(len(chunks), 1)

    def test_semantic_retriever(self):
        retriever = SemanticRetriever()
        retriever.index(self.sample_docs)
        results = retriever.retrieve("What is RAG?", top_k=2)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("Retrieval-Augmented Generation", results[0]["text"])

    def test_keyword_retriever(self):
        retriever = KeywordRetriever()
        retriever.index(self.sample_docs)
        results = retriever.retrieve("PostgreSQL database system", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("PostgreSQL", results[0]["text"])

    def test_hybrid_retriever(self):
        retriever = HybridRetriever()
        retriever.index(self.sample_docs)
        results = retriever.retrieve("hybrid search reciprocal rank fusion", top_k=2)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["retrieval_method"], "hybrid_rrf")

    def test_reranker(self):
        reranker = Reranker()
        candidates = [
            {"text": "Completely unrelated text about cooking apples and oranges."},
            {"text": "FastAPI is a Python web framework designed for high speed and automatic OpenAPI documentation."},
        ]
        reranked = reranker.rerank("Tell me about FastAPI framework", candidates, top_k=2)
        self.assertEqual(len(reranked), 2)
        self.assertIn("FastAPI", reranked[0]["text"])

    def test_rag_pipeline_end_to_end(self):
        pipeline = RAGPipeline()
        pipeline.clear()
        res_ingest = pipeline.ingest_raw_text(
            "Vector databases store high-dimensional embeddings for nearest neighbor search."
        )
        self.assertGreater(res_ingest["chunks_created"], 0)

        query_res = pipeline.query("What do vector databases store?", retriever_type="hybrid")
        self.assertIn("question", query_res)
        self.assertIn("answer", query_res)
        self.assertGreaterEqual(len(query_res["sources"]), 1)


if __name__ == "__main__":
    unittest.main()
