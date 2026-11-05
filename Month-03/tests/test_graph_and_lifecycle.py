import unittest
import sys
import os

day17 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-17", "AI"))
day18 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-18", "AI"))
day20 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-20", "AI"))
day21 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-21", "AI"))

for p in [day17, day18, day20, day21]:
    sys.path.insert(0, p)

from multi_hop_rag import MultiHopRAG
from build_graph import KnowledgeGraph
from incremental_indexer import IncrementalIndexer
from delete_document_pipeline import DocumentDeletionCoordinator


class TestGraphAndLifecycle(unittest.TestCase):
    def test_multi_hop_rag_chaining(self):
        kb = [
            {"id": "doc1", "text": "Google researchers published Attention is All You Need introducing the transformer."},
            {"id": "doc2", "text": "Sundar Pichai serves as CEO of Google."}
        ]
        rag = MultiHopRAG(kb)
        res = rag.execute_two_hop_query("Who is CEO of company that created transformer?")
        self.assertEqual(res["hop_1"]["extracted_fact"], "Google")
        self.assertIn("Sundar Pichai", res["synthesized_answer"])
        self.assertEqual(len(res["provenance_chain"]), 2)

    def test_knowledge_graph_subgraph(self):
        kg = KnowledgeGraph()
        kg.add_relationship("FastAPI", "USED_BY", "ProductionRAG")
        kg.add_relationship("ProductionRAG", "USES", "Qdrant")
        sub = kg.get_subgraph("FastAPI", max_depth=2)
        self.assertIn("Qdrant", sub["connected_entities"])
        self.assertIn("ProductionRAG", sub["connected_entities"])
        self.assertEqual(len(sub["relationships"]), 2)

    def test_incremental_indexer(self):
        indexer = IncrementalIndexer()
        chunks = [{"chunk_id": "c1", "text": "Initial version of clause 1."}]
        res1 = indexer.index_document("doc1", chunks)
        self.assertEqual(res1["added_chunks"], 1)

        # Same chunk -> should detect unchanged
        res2 = indexer.index_document("doc1", chunks)
        self.assertEqual(res2["unchanged_chunks"], 1)
        self.assertEqual(res2["added_chunks"], 0)

    def test_deletion_coordinator(self):
        coord = DocumentDeletionCoordinator()
        coord.ingest_document("d99", "secret payload", ["ch1", "ch2"])
        self.assertFalse(coord.verify_no_stale_vectors("d99"))

        del_res = coord.delete_document_cascade("d99")
        self.assertEqual(del_res["status"], "PURGED_SUCCESSFULLY")
        self.assertTrue(coord.verify_no_stale_vectors("d99"))


if __name__ == "__main__":
    unittest.main()
