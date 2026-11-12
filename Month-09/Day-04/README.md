# 📅 Day 04 — Tensor Parallelism (Megatron TP) & Prim's MST

## Overview
Architecting intra-node Tensor Parallelism with Column and Row parallel linear projections alongside solving LeetCode 1584 (Min Cost to Connect All Points) using Prim's Minimum Spanning Tree.

## Components
- `AI/megatron_tensor_parallel.py`: Column and row parallel weight matrices, GeLU non-linear preservation, and single All-Reduce fusion.
- `DSA/PrimsMinimumSpanningTree.java`: $O(E \log V)$ Prim's MST algorithm with greedy cut-property min-heap.
- `Interview/technical_questions.md`: Megatron-LM two-communication Transformer layer proof and the Cut Property.
- `Notes/notes.md`: NVLink hardware boundaries and Prim's algorithmic complexity.
