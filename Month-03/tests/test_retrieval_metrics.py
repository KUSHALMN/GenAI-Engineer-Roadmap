import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-27", "AI"))
sys.path.insert(0, day_path)

from retrieval_metrics import RetrievalMetrics

class TestRetrievalMetrics(unittest.TestCase):
    def test_precision_recall_k(self):
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        ground_truth = {"d1", "d3"}

        p3 = RetrievalMetrics.precision_at_k(retrieved, ground_truth, k=3)
        self.assertAlmostEqual(p3, 2.0 / 3.0, places=3)

        r3 = RetrievalMetrics.recall_at_k(retrieved, ground_truth, k=3)
        self.assertAlmostEqual(r3, 1.0, places=3)

    def test_mrr(self):
        retrieved = ["d9", "d1", "d3"]
        ground_truth = {"d1"}
        rr = RetrievalMetrics.reciprocal_rank(retrieved, ground_truth)
        self.assertAlmostEqual(rr, 0.5, places=3)

    def test_ndcg_at_k(self):
        retrieved = ["d1", "d2"]
        relevances = {"d1": 3.0, "d2": 1.0}
        ndcg = RetrievalMetrics.ndcg_at_k(retrieved, relevances, k=2)
        self.assertAlmostEqual(ndcg, 1.0, places=3)

if __name__ == "__main__":
    unittest.main()
