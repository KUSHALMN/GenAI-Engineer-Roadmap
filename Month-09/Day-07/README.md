# 📅 Day 07 — PyTorch FSDP & Segment Tree RMQ

## Overview
Modeling PyTorch Fully Sharded Data Parallel (FSDP) and Activation Checkpointing memory dynamics alongside implementing an $O(\log N)$ Segment Tree for Range Minimum Queries (RMQ).

## Components
- `AI/fsdp_activation_checkpointing.py`: Layer-by-layer unsharding, recomputation trade-off calculations, and peak VRAM profiling.
- `DSA/SegmentTreeRangeMinimumQuery.java`: Segment tree construction ($O(N)$), point updates ($O(\log N)$), and range queries ($O(\log N)$).
- `Interview/technical_questions.md`: FSDP forward/backward hook mechanics and 4N segment tree size derivation.
- `Notes/notes.md`: Recomputation efficiency and 0-based binary tree indexing.
