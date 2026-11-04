import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-09", "AI"))
sys.path.insert(0, day_path)

from hybrid_search_engine import HybridSearchEngine

class TestHybridSearch(unittest.TestCase):
    def setUp(self):
        self.docs = [
            {"id": "d1", "text": "PostgreSQL database with vector search"},
            {"id": "d2", "text": "Elasticsearch inverted index BM25 search"}
        ]
        self.engine = HybridSearchEngine(self.docs)

    def test_rrf_ranking(self):
        results = self.engine.search_rrf("PostgreSQL vector", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "d1")
        self.assertIn("rrf_score", results[0])

    def test_weighted_ranking(self):
        results = self.engine.search_weighted("Elasticsearch BM25", dense_weight=0.2, top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "d2")

if __name__ == "__main__":
    unittest.main()
