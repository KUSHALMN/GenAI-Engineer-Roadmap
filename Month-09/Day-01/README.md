# 📅 Day 01 — BPE Tokenizer Pretraining & 0/1 Knapsack DP

## Overview
Building a Byte-Pair Encoding (BPE) tokenizer from scratch with byte-fallback and special token handling alongside solving LeetCode 416 (Partition Equal Subset Sum) with space-optimized DP.

## Components
- `AI/bpe_tokenizer_trainer.py`: Byte-level BPE vocabulary training, iterative pair merges, and reversible string encoding/decoding.
- `DSA/KnapsackZeroOneTimedSet.java`: $O(N \cdot Target)$ time, $O(Target)$ space 1D dynamic programming solution.
- `Interview/technical_questions.md`: Architectural comparison of tokenizers and reverse DP traversal proof.
- `Notes/notes.md`: Vocabulary compression bounds and subset sum invariants.
