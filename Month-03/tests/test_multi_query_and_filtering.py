import unittest
import sys
import os

day11_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-11", "AI"))
day12_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-12", "AI"))
day14_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-14", "AI"))
day15_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-15", "AI"))

for p in [day11_path, day12_path, day14_path, day15_path]:
    sys.path.insert(0, p)

from multi_query_retriever import MultiQueryRetriever
from hyde_retriever import HyDERetriever
from context_compressor import ContextCompressor
from filtered_hybrid_retriever import FilteredHybridRetriever


class TestRetrievalPipelineComponents(unittest.TestCase):
    def test_multi_query_deduplication(self):
        docs = [
            {"id": "c1", "text": "HNSW vector indexing and approximate nearest neighbors."},
            {"id": "c2", "text": "BM25 inverted indexes for keyword search."}
        ]
        mq = MultiQueryRetriever(docs)
        res = mq.retrieve_and_deduplicate("vector indexing", top_k_per_query=2)
        self.assertGreater(len(res["generated_subqueries"]), 1)
        self.assertLessEqual(len(res["results"]), len(docs))
        # Ensure no duplicate doc IDs
        ids = [r["id"] for r in res["results"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_hyde_retriever(self):
        docs = [
            {"id": "d1", "text": "PostgreSQL relational databases support pgvector extension."},
            {"id": "d2", "text": "Unrelated culinary recipes."}
        ]
        hyde = HyDERetriever(docs)
        res = hyde.search_hyde("How to run pgvector in PostgreSQL?", top_k=1)
        self.assertEqual(res["results"][0]["id"], "d1")
        self.assertIn("PostgreSQL", res["hypothetical_document"])

    def test_context_compression(self):
        compressor = ContextCompressor(min_similarity_threshold=0.2)
        chunk = {
            "id": "c100",
            "text": "The quick brown fox. Vector database HNSW indexing delivers logarithmic speed. Office party on Friday.",
            "metadata": {"page": 2}
        }
        res = compressor.compress_chunk("HNSW indexing logarithmic speed", chunk)
        self.assertIn("HNSW", res["compressed_text"])
        self.assertEqual(res["source_id"], "c100")
        self.assertGreater(res["compression_ratio"], 0.0)

    def test_filtered_hybrid(self):
        docs = [
            {"id": "d_acme", "text": "Acme engineering roadmap", "metadata": {"tenant_id": "acme", "department": "eng"}},
            {"id": "d_beta", "text": "Beta competitor document", "metadata": {"tenant_id": "beta", "department": "eng"}}
        ]
        f_retriever = FilteredHybridRetriever(docs)
        res = f_retriever.search("roadmap", filters={"tenant_id": "acme"})
        self.assertEqual(len(res["returned_results"]), 1)
        self.assertEqual(res["returned_results"][0]["id"], "d_acme")
        self.assertEqual(res["filtered_out_docs"], 1)


if __name__ == "__main__":
    unittest.main()
