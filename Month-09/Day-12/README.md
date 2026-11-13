# 📅 Day 12 — Sequence Parallelism (Megatron-SP) & Hierholzer's Algorithm

## Overview
Simulating Megatron-LM Sequence Parallelism (SP) activation sharding ($s / tp$) and communication fusion alongside solving LeetCode 332 (Reconstruct Itinerary) using Hierholzer's Eulerian Path algorithm.

## Components
- `AI/megatron_sequence_parallel.py`: Activation memory reduction analysis, All-Gather forward, and Reduce-Scatter backward flow modeling.
- `DSA/HierholzersEulerianPath.java`: $O(E \log E)$ Hierholzer's algorithm with min-heap lexicographical ordering and post-order traversal.
- `Interview/technical_questions.md`: Communication split equivalence (All-Reduce $\leftrightarrow$ Reduce-Scatter + All-Gather) and Eulerian post-order proofs.
- `Notes/notes.md`: Megatron-SP vs DeepSpeed-Ulysses and degree parity conditions.
