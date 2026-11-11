"""
Model and Retrieval Experiment Tracking: Multi-Parameter Experiment Manifests,
Embedding Model Comparisons, Chunking Configurations, and Metric Logging.
"""

from dataclasses import dataclass, field
import time
from typing import List


@dataclass
class ExperimentRunRecord:
    experiment_id: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    reranker_enabled: bool
    ndcg_at_10: float
    recall_at_5: float
    avg_latency_ms: float
    timestamp: float = field(default_factory=time.time)


class ExperimentTrackingManager:
    def __init__(self):
        self.runs: List[ExperimentRunRecord] = []

    def record_run(self, run: ExperimentRunRecord):
        self.runs.append(run)

    def find_best_configuration(self, metric: str = "ndcg_at_10") -> ExperimentRunRecord:
        return max(self.runs, key=lambda r: getattr(r, metric))


if __name__ == "__main__":
    tracker = ExperimentTrackingManager()
    r1 = ExperimentRunRecord("exp_01", "text-embedding-3-small", 512, 50, 5, False, 0.81, 0.85, 35.0)
    r2 = ExperimentRunRecord("exp_02", "bge-large-en-v1.5", 512, 50, 5, True, 0.92, 0.94, 55.0)
    tracker.record_run(r1)
    tracker.record_run(r2)

    best = tracker.find_best_configuration("ndcg_at_10")
    assert best.experiment_id == "exp_02"
    assert best.ndcg_at_10 == 0.92

    print("=== Day 10: Experiment Tracking Manifest ===")
    print(f"Top Experiment: {best.experiment_id} | Model: {best.embedding_model} | NDCG@10: {best.ndcg_at_10}")
