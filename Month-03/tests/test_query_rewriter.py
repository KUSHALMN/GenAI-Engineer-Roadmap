import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-10", "AI"))
sys.path.insert(0, day_path)

from query_rewriter import QueryRewriter

class TestQueryRewriter(unittest.TestCase):
    def setUp(self):
        self.rewriter = QueryRewriter()

    def test_filler_removal(self):
        cleaned = self.rewriter.clean_filler_words("Please tell me about Pinecone")
        self.assertNotIn("please", cleaned.lower())

    def test_coreference_resolution(self):
        history = [
            {"role": "user", "content": "Tell me about Pinecone vector database."},
            {"role": "assistant", "content": "Pinecone is an enterprise vector database."}
        ]
        res = self.rewriter.rewrite("How does it scale?", history)
        self.assertTrue(res["resolved_coreference"])
        self.assertIn("Pinecone", res["rewritten_query"])

    def test_acronym_expansion(self):
        expanded = self.rewriter.expand_acronyms("deploy rag on k8s")
        self.assertIn("kubernetes", expanded.lower())
        self.assertIn("retrieval augmented generation", expanded.lower())

if __name__ == "__main__":
    unittest.main()
