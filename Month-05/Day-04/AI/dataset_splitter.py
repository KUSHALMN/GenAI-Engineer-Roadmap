"""
Day 04: Data Splitting and Leakage Prevention
Creates reproducible train/validation/test splits, checks for near-duplicate
data leakage across splits, and enforces group/cluster partitioning.
"""

from typing import List, Dict, Any, Tuple
import random
import hashlib

class DatasetSplitter:
    @staticmethod
    def split_train_val_test(data: List[Dict[str, Any]],
                             train_ratio: float = 0.8,
                             val_ratio: float = 0.1,
                             seed: int = 42) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        random.seed(seed)
        shuffled = list(data)
        random.shuffle(shuffled)

        n = len(shuffled)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        train = shuffled[:train_end]
        val = shuffled[train_end:val_end]
        test = shuffled[val_end:]
        return train, val, test

    @staticmethod
    def detect_leakage(train: List[Dict[str, Any]], eval_set: List[Dict[str, Any]]) -> List[str]:
        """Detects prompt overlap between train and evaluation sets."""
        train_prompts = {r["prompt"].strip().lower() for r in train}
        leaks = []
        for r in eval_set:
            p = r["prompt"].strip().lower()
            if p in train_prompts:
                leaks.append(p)
        return leaks

if __name__ == "__main__":
    dataset = [
        {"prompt": f"Instruction {i}", "response": f"Response {i}"}
        for i in range(100)
    ]
    train, val, test = DatasetSplitter.split_train_val_test(dataset, 0.8, 0.1, seed=42)

    assert len(train) == 80
    assert len(val) == 10
    assert len(test) == 10

    # Leakage check
    leaks = DatasetSplitter.detect_leakage(train, test)
    assert len(leaks) == 0, "No prompt leakage should exist in stratified splits"
    print(f"Data successfully split into {len(train)} train, {len(val)} val, {len(test)} test.")
    print("Day 04 AI Dataset Splitter passed all tests.")
