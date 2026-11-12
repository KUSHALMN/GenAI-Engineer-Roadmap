# 📅 Day 06 — ZeRO-1, 2, 3 Memory Optimization & Wildcard Trie

## Overview
Simulating DeepSpeed ZeRO-1, ZeRO-2, and ZeRO-3 memory partitioning across mixed-precision clusters alongside solving LeetCode 211 (Design Add and Search Words Data Structure) via recursive Trie DFS.

## Components
- `AI/zero_memory_partitioner.py`: 16-byte parameter breakdown, stage 1/2/3 partitioning formulas, and cluster VRAM scaling.
- `DSA/TrieWildcardAutocomplete.java`: Trie with '.' wildcard recursive DFS backtracking.
- `Interview/technical_questions.md`: Mathematical derivations of ZeRO stages and wildcard tree branching analysis.
- `Notes/notes.md`: ZeRO-Offload architecture and Trie stack depth bounds.
