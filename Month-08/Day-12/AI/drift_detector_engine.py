"""
Data and Concept Drift Detection: Vocabulary Frequency Shifts, Query Length Tracking,
and Embedding Centroid Distance Measurement.
"""

import math
from typing import Dict, List


class DriftDetectorEngine:
    def compute_centroid(self, vectors: List[List[float]]) -> List[float]:
        if not vectors:
            return []
        dim = len(vectors[0])
        centroid = [0.0] * dim
        for v in vectors:
            for i in range(dim):
                centroid[i] += v[i]
        return [c / len(vectors) for c in centroid]

    def euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def detect_semantic_drift(self, baseline_vectors: List[List[float]], current_vectors: List[List[float]], threshold: float = 0.25) -> Dict[str, float]:
        c1 = self.compute_centroid(baseline_vectors)
        c2 = self.compute_centroid(current_vectors)
        dist = self.euclidean_distance(c1, c2)
        return {
            "centroid_distance": round(dist, 4),
            "is_drift_detected": dist >= threshold
        }


if __name__ == "__main__":
    detector = DriftDetectorEngine()
    baseline = [[0.1, 0.2], [0.12, 0.18], [0.11, 0.21]]
    current_stable = [[0.11, 0.19], [0.13, 0.22]]
    current_drifted = [[0.8, 0.9], [0.85, 0.95]]

    stable_res = detector.detect_semantic_drift(baseline, current_stable, threshold=0.25)
    assert stable_res["is_drift_detected"] is False

    drift_res = detector.detect_semantic_drift(baseline, current_drifted, threshold=0.25)
    assert drift_res["is_drift_detected"] is True

    print("=== Day 12: Drift Detector Engine ===")
    print(f"Centroid Distance: {drift_res['centroid_distance']} | Drift Detected: {drift_res['is_drift_detected']}")
