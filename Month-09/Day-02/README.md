# 📅 Day 02 — Sharded Streaming DataLoaders & Bellman-Ford

## Overview
Designing binary memory-mapped distributed token streaming loaders for trillion-token pretraining alongside solving LeetCode 787 (Cheapest Flights Within K Stops) via bounded Bellman-Ford relaxation.

## Components
- `AI/sharded_streaming_dataloader.py`: Binary shard packing, deterministic rank hashing, and continuous sequence chunking.
- `DSA/BellmanFordShortestPath.java`: $O(K \cdot E)$ time bounded Bellman-Ford algorithm with frozen array copies.
- `Interview/technical_questions.md`: Multi-terabyte mmap mechanics and path length relaxation constraints.
- `Notes/notes.md`: Storage packing efficiency and Bellman-Ford edge relaxation invariants.
