import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-13", "AI"))
sys.path.insert(0, day_path)

from reranker_pipeline import CrossEncoderReranker

class TestRerankerPipeline(unittest.TestCase):
    def setUp(self):
        self.reranker = CrossEncoderReranker()
        self.candidates = [
            {"id": "doc_1", "text": "Python has decorators, generators, and dynamic typing."},
            {"id": "doc_2", "text": "Cross-encoder models pass the query and candidate chunk together into attention layers."}
        ]

    def test_cross_attention_scoring(self):
        query = "cross-encoder attention layers"
        ranked = self.reranker.rerank(query, self.candidates, top_n=2)
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0]["id"], "doc_2")
        self.assertGreater(ranked[0]["rerank_score"], ranked[1]["rerank_score"])

if __name__ == "__main__":
    unittest.main()
