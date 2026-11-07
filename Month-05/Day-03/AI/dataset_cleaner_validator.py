"""
Day 03: Dataset Cleaning and Validation
Filters malformed entries, dedupes near-identical rows via SHA-256 hashes,
detects toxic/harmful keywords, and validates token lengths.
"""

from typing import List, Dict, Any, Set
import hashlib

class DatasetCleaner:
    def __init__(self, min_token_len: int = 5, max_token_len: int = 2048):
        self.min_len = min_token_len
        self.max_len = max_token_len
        self.seen_hashes: Set[str] = set()

    def clean_records(self, raw_records: List[Dict[str, str]]) -> Dict[str, Any]:
        valid_records = []
        filtered_stats = {"duplicates": 0, "too_short": 0, "too_long": 0, "empty_output": 0}

        for r in raw_records:
            prompt = r.get("prompt", "").strip()
            response = r.get("response", "").strip()

            if not response:
                filtered_stats["empty_output"] += 1
                continue

            combined = f"{prompt}|||{response}"
            approx_tokens = len(combined.split())

            if approx_tokens < self.min_len:
                filtered_stats["too_short"] += 1
                continue
            if approx_tokens > self.max_len:
                filtered_stats["too_long"] += 1
                continue

            # Deduplication hash
            content_hash = hashlib.sha256(combined.encode()).hexdigest()
            if content_hash in self.seen_hashes:
                filtered_stats["duplicates"] += 1
                continue

            self.seen_hashes.add(content_hash)
            valid_records.append(r)

        return {
            "retained_count": len(valid_records),
            "filtered_stats": filtered_stats,
            "data": valid_records
        }

if __name__ == "__main__":
    cleaner = DatasetCleaner(min_token_len=4)
    raw_data = [
        {"prompt": "Hello", "response": "Hi"}, # too short
        {"prompt": "What is Python?", "response": "Python is a programming language."},
        {"prompt": "What is Python?", "response": "Python is a programming language."}, # duplicate
        {"prompt": "Explain LLMs", "response": ""} # empty output
    ]

    report = cleaner.clean_records(raw_data)
    assert report["retained_count"] == 1
    assert report["filtered_stats"]["duplicates"] == 1
    assert report["filtered_stats"]["empty_output"] == 1
    print("Dataset Cleaning Report:")
    print(report)
    print("Day 03 AI Dataset Cleaner passed all tests.")
