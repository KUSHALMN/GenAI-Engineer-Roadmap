import unittest
import sys
import os

day24 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-24", "AI"))
day25 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-25", "AI"))
day28 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-28", "AI"))
day31 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-31", "AI"))

for p in [day24, day25, day28, day31]:
    sys.path.insert(0, p)

from query_router import QueryRouter
from retrieval_cache import RetrievalCache
from ablation_runner import AblationExperimentRunner
from enterprise_rag_benchmark import EnterpriseRAGPipeline


class TestRouterCacheBenchmark(unittest.TestCase):
    def test_query_router_classification(self):
        router = QueryRouter()
        r1 = router.route_query("Hello there")
        self.assertEqual(r1["route"], "DIRECT_LLM")

        r2 = router.route_query("Average salary count of engineers")
        self.assertEqual(r2["route"], "STRUCTURED_SQL")

        r3 = router.route_query("Error 0x80070005 in module AUTH-101")
        self.assertEqual(r3["route"], "KEYWORD_BM25")

    def test_retrieval_cache_invalidation(self):
        cache = RetrievalCache(ttl_seconds=10)
        key = cache.generate_cache_key("query", "tenant1", "m1", "v1.0", {})
        cache.put(key, ["result_data"], "tenant1", "v1.0")

        self.assertEqual(cache.get(key), ["result_data"])
        self.assertEqual(cache.get_hit_ratio(), 1.0)

        # Invalidate index version
        cache.invalidate_by_index_version("v1.0")
        self.assertIsNone(cache.get(key))

    def test_ablation_experiment_runner(self):
        runner = AblationExperimentRunner()
        config = {"name": "test_exp", "chunk_size": 512, "dense_weight": 0.6, "top_k": 5, "rerank": True}
        res = runner.run_trial(config)
        self.assertEqual(res["experiment_name"], "test_exp")
        self.assertGreater(res["recall_at_k"], 0.0)
        self.assertGreater(res["latency_p95_ms"], 0.0)

    def test_enterprise_rag_pipeline_capstone(self):
        pipeline = EnterpriseRAGPipeline()
        pipeline.ingest("doc_1", "Production Kubernetes cluster deployment guide.", "tenant_corp", "engineering")
        
        # Test authorized retrieval
        res = pipeline.run_pipeline("Kubernetes deployment guide", "tenant_corp", "engineering")
        self.assertEqual(res["status"], "GROUNDED_SUCCESS")
        self.assertEqual(len(res["citations"]), 1)

        # Test cross-tenant isolation
        res_blocked = pipeline.run_pipeline("Kubernetes deployment guide", "other_tenant", "engineering")
        self.assertEqual(res_blocked["status"], "ABSTAINED_SAFELY")


if __name__ == "__main__":
    unittest.main()
