# 📅 Day 03 — DDP Ring All-Reduce & Floyd-Warshall

## Overview
Simulating the bandwidth-optimal NCCL Ring All-Reduce protocol for Distributed Data Parallelism alongside mastering Floyd-Warshall All-Pairs Shortest Path (LeetCode 1334).

## Components
- `AI/ddp_ring_allreduce.py`: Two-phase Scatter-Reduce and All-Gather simulation across virtual GPU ring ranks.
- `DSA/FloydWarshallAllPairs.java`: $O(V^3)$ time, $O(V^2)$ space dynamic programming all-pairs shortest path.
- `Interview/technical_questions.md`: Ring All-Reduce bandwidth optimality proof and Floyd-Warshall outermost loop invariant.
- `Notes/notes.md`: Gradient bucketing overlap and arithmetic overflow prevention.
