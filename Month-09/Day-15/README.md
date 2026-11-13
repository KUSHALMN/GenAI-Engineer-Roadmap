# 📅 Day 15 — Distributed Async Checkpointing & Maximal Rectangle DP

## Overview
Designing distributed asynchronous sharded checkpointing (PyTorch DCP) with zero GPU downtime alongside solving LeetCode 85 (Maximal Rectangle) using dynamic programming and monotonic stacks.

## Components
- `AI/distributed_async_checkpointing.py`: Parallel shard writing, tensor slice metadata manifests, and asynchronous I/O offloading.
- `DSA/MaximalRectangleTimedSet.java`: $O(R \cdot C)$ time, $O(C)$ space matrix reduction to monotonic histogram stacks.
- `Interview/technical_questions.md`: DCP parallel I/O architecture and 2D-to-1D reduction proofs.
- `Notes/notes.md`: Dynamic cluster resharding and memory reuse techniques.
