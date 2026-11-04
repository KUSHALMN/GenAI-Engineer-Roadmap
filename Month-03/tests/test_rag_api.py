import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-29", "AI"))
sys.path.insert(0, day_path)

from rag_api_service import ProductionRAGService

class TestRAGApiService(unittest.TestCase):
    def setUp(self):
        self.service = ProductionRAGService()

    def test_health_check(self):
        res = self.service.health_check()
        self.assertEqual(res["status"], "HEALTHY")
        self.assertEqual(res["service"], "Production-RAG-v2")

    def test_ingest_and_query_flow(self):
        ingest_res = self.service.ingest_endpoint({
            "doc_id": "test_doc",
            "chunks": [
                {"chunk_id": "c1", "text": "HNSW index accelerates vector similarity search."},
                {"chunk_id": "c2", "text": "PostgreSQL provides relational database transactions."}
            ]
        })
        self.assertEqual(ingest_res["status_code"], 201)

        query_res = self.service.query_endpoint({
            "query": "HNSW vector search",
            "tenant_id": "tenant_1",
            "top_k": 1
        })
        self.assertEqual(query_res["status_code"], 200)
        self.assertGreater(len(query_res["citations"]), 0)
        self.assertEqual(query_res["citations"][0]["chunk_id"], "c1")

    def test_feedback_endpoint(self):
        fb_res = self.service.feedback_endpoint({
            "query_id": "q101",
            "rating": 1,
            "comment": "Good answer"
        })
        self.assertEqual(fb_res["status_code"], 200)
        self.assertEqual(fb_res["status"], "FEEDBACK_RECORDED")

if __name__ == "__main__":
    unittest.main()
