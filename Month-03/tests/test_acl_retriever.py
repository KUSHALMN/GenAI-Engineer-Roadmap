import unittest
import sys
import os

day_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Day-22", "AI"))
sys.path.insert(0, day_path)

from acl_retriever import ACLRetriever, UserSecurityContext

class TestACLRetriever(unittest.TestCase):
    def setUp(self):
        self.docs = [
            {
                "id": "doc_eng",
                "text": "Kubernetes cluster architecture details.",
                "metadata": {"tenant_id": "corp_a", "allowed_roles": ["engineer"]}
            },
            {
                "id": "doc_hr",
                "text": "Executive compensation salary packages.",
                "metadata": {"tenant_id": "corp_a", "allowed_roles": ["hr_exec"]}
            },
            {
                "id": "doc_ext",
                "text": "External partner secrets.",
                "metadata": {"tenant_id": "corp_b", "is_public_in_tenant": True}
            }
        ]
        self.retriever = ACLRetriever(self.docs)

    def test_authorized_access(self):
        eng = UserSecurityContext(user_id="u1", tenant_id="corp_a", roles=["engineer"])
        res = self.retriever.retrieve_secure("Kubernetes architecture", eng)
        self.assertEqual(len(res["authorized_results"]), 1)
        self.assertEqual(res["authorized_results"][0]["id"], "doc_eng")

    def test_cross_tenant_denial(self):
        eng = UserSecurityContext(user_id="u1", tenant_id="corp_a", roles=["engineer", "admin"])
        res = self.retriever.retrieve_secure("partner secrets", eng)
        self.assertEqual(len(res["authorized_results"]), 0)
        self.assertEqual(res["unauthorized_chunks_blocked"], 3)

if __name__ == "__main__":
    unittest.main()
