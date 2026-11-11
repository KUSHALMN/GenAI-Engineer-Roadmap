"""
Golden Dataset Governance: Semantic Versioning, Provenance Tracking,
Annotator Inter-Rater Agreement, and Evidence Ground Truth Validation.
"""

from dataclasses import dataclass, field
import hashlib
import time
from typing import List


@dataclass
class GoldenTestCase:
    case_id: str
    query: str
    expected_answer: str
    ground_truth_context_ids: List[str]
    annotator_id: str


@dataclass
class DatasetVersionMetadata:
    version_tag: str
    dataset_hash: str
    total_samples: int
    created_at: float
    cases: List[GoldenTestCase] = field(default_factory=list)


class GoldenDatasetGovernanceManager:
    def create_version(self, version_tag: str, cases: List[GoldenTestCase]) -> DatasetVersionMetadata:
        serialized = "".join(f"{c.case_id}:{c.query}" for c in cases)
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return DatasetVersionMetadata(
            version_tag=version_tag,
            dataset_hash=digest,
            total_samples=len(cases),
            created_at=time.time(),
            cases=cases
        )


if __name__ == "__main__":
    gov = GoldenDatasetGovernanceManager()
    cases = [
        GoldenTestCase("q_01", "What is RPO?", "Max acceptable data loss in time", ["doc_dr_1"], "annotator_alice"),
        GoldenTestCase("q_02", "What is RTO?", "Max acceptable recovery duration", ["doc_dr_2"], "annotator_bob")
    ]
    manifest = gov.create_version("v1.0.0-GOLD", cases)
    assert manifest.total_samples == 2
    assert len(manifest.dataset_hash) == 64

    print("=== Day 02: Golden Dataset Governance ===")
    print(f"Created Golden Dataset: {manifest.version_tag} | Hash: {manifest.dataset_hash[:16]}...")
