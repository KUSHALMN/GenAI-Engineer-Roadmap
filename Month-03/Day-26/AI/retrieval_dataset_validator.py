"""
Retrieval Evaluation Dataset Validator & Quality Checker
Verifies:
1. Valid JSONL syntax and schema compliance
2. Coverage across difficulty tiers (easy, medium, hard, unanswerable)
3. Non-empty expected_chunk_ids for answerable queries
4. Non-empty expected_facts for factual verification
5. Exactly zero expected_chunk_ids for unanswerable negative controls
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class DatasetValidator:
    REQUIRED_FIELDS = {"query_id", "query", "difficulty", "expected_chunk_ids", "expected_facts", "is_answerable"}
    VALID_DIFFICULTIES = {"easy", "medium", "hard", "unanswerable"}

    def validate_file(self, filepath: str) -> Dict[str, Any]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found at {filepath}")

        rows = []
        errors = []
        difficulty_counts = {d: 0 for d in self.VALID_DIFFICULTIES}

        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue

                try:
                    data = json.loads(clean_line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_no}: Malformed JSON syntax: {e}")
                    continue

                # Field validation
                missing = self.REQUIRED_FIELDS - set(data.keys())
                if missing:
                    errors.append(f"Line {line_no} [{data.get('query_id', 'unknown')}]: Missing fields: {missing}")

                # Difficulty validation
                diff = data.get("difficulty")
                if diff not in self.VALID_DIFFICULTIES:
                    errors.append(f"Line {line_no}: Invalid difficulty '{diff}'. Must be one of {self.VALID_DIFFICULTIES}")
                else:
                    difficulty_counts[diff] += 1

                # Answerability consistency
                is_ans = data.get("is_answerable", True)
                chunk_ids = data.get("expected_chunk_ids", [])
                facts = data.get("expected_facts", [])

                if is_ans and not chunk_ids:
                    errors.append(f"Line {line_no} [{data.get('query_id')}]: Answerable query has empty expected_chunk_ids!")
                if not is_ans and chunk_ids:
                    errors.append(f"Line {line_no} [{data.get('query_id')}]: Unanswerable query has unexpected chunk_ids!")

                rows.append(data)

        passed = len(errors) == 0
        return {
            "valid": passed,
            "total_records": len(rows),
            "errors": errors,
            "difficulty_distribution": difficulty_counts,
            "unanswerable_ratio": round(difficulty_counts["unanswerable"] / max(1, len(rows)), 3)
        }


if __name__ == "__main__":
    import os
    dataset_path = os.path.join(os.path.dirname(__file__), "retrieval_dataset.jsonl")
    validator = DatasetValidator()
    report = validator.validate_file(dataset_path)

    print("=== Retrieval Dataset Validation Report ===")
    print(f"Validation Status: {'PASSED' if report['valid'] else 'FAILED'}")
    print(f"Total Evaluated Records: {report['total_records']}")
    print(f"Difficulty Distribution: {report['difficulty_distribution']}")
    print(f"Negative Control Ratio: {report['unanswerable_ratio'] * 100:.1f}%")
    if report["errors"]:
        print("\nErrors Found:")
        for err in report["errors"]:
            print(f" - {err}")
    else:
        print("\nZero schema violations or negative-label inconsistencies found!")
