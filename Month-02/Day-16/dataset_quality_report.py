"""
Dataset Quality Report Generator & Train/Val Split Tool.
Calculates token length statistics (mean, p50, p95), vocabulary diversity,
PII density, duplicate rate, and performs reproducible train/val splits.
"""

import math
import random
from typing import Any, Dict, List, Tuple
from deduplicator import Deduplicator
from pii_scrubber import DatasetPIIScrubber


class DatasetQualityAnalyzer:

    @staticmethod
    def calculate_percentiles(values: List[int]) -> Dict[str, float]:
        if not values:
            return {"mean": 0, "p50": 0, "p95": 0, "max": 0}
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mean_val = sum(sorted_vals) / n
        p50 = sorted_vals[int(round(0.50 * (n - 1)))]
        p95 = sorted_vals[int(round(0.95 * (n - 1)))]
        return {
            "mean": round(mean_val, 1),
            "p50": p50,
            "p95": p95,
            "max": sorted_vals[-1],
        }

    @classmethod
    def generate_report(cls, records: List[Dict[str, Any]], text_key: str = "text") -> Dict[str, Any]:
        """Analyzes quality metrics of dataset."""
        total_records = len(records)
        if total_records == 0:
            return {"error": "Dataset is empty"}

        # Token & character metrics
        char_lengths = [len(r.get(text_key, "")) for r in records]
        token_lengths = [max(1, len(r.get(text_key, "").split())) for r in records]

        # Vocabulary
        vocab = set()
        for r in records:
            vocab.update(r.get(text_key, "").lower().split())

        # Duplicate check
        _, dup_count = Deduplicator.exact_deduplicate(records, text_key=text_key)

        # PII check
        _, pii_summary = DatasetPIIScrubber.scrub_dataset(records, text_key=text_key)

        return {
            "overview": {
                "total_records": total_records,
                "unique_vocabulary_size": len(vocab),
                "exact_duplicates": dup_count,
                "duplicate_rate_pct": round((dup_count / total_records) * 100, 2),
            },
            "token_length_distribution": cls.calculate_percentiles(token_lengths),
            "character_length_distribution": cls.calculate_percentiles(char_lengths),
            "privacy_metrics": {
                "records_with_pii": pii_summary["records_with_pii"],
                "pii_rate_pct": pii_summary["pii_record_rate_pct"],
                "entities_found": pii_summary["pii_entity_breakdown"],
            },
        }

    @staticmethod
    def train_validation_split(
        records: List[Dict[str, Any]],
        val_ratio: float = 0.20,
        seed: int = 42,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Performs reproducible train/validation split."""
        shuffled = list(records)
        random.seed(seed)
        random.shuffle(shuffled)

        val_size = int(round(len(shuffled) * val_ratio))
        val_set = shuffled[:val_size]
        train_set = shuffled[val_size:]
        return train_set, val_set


if __name__ == "__main__":
    sample_data = [
        {"id": 1, "text": "Supervised fine tuning adapts large models to custom enterprise domain tasks."},
        {"id": 2, "text": "Contact admin at dev@company.org for access tokens and credentials."},
        {"id": 3, "text": "Reinforcement learning from human feedback aligns completions with intent."},
        {"id": 4, "text": "Supervised fine tuning adapts large models to custom enterprise domain tasks."},  # dup
        {"id": 5, "text": "Direct preference optimization provides an offline alternative to PPO."},
    ]

    report = DatasetQualityAnalyzer.generate_report(sample_data)
    print("Quality Report Summary:", report["overview"])
    assert report["overview"]["exact_duplicates"] == 1
    assert report["privacy_metrics"]["records_with_pii"] == 1

    train, val = DatasetQualityAnalyzer.train_validation_split(sample_data, val_ratio=0.2, seed=42)
    assert len(train) == 4
    assert len(val) == 1
    print("DatasetQualityAnalyzer tests passed successfully!")
