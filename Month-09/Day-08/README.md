# 📅 Day 08 — 3D Parallelism Orchestrator & Kahn's Topological Sort

## Overview
Architecting 3D Parallelism cluster grids (DP $\times$ TP $\times$ PP) and communicator process group topologies alongside implementing LeetCode 210 (Course Schedule II) using Kahn's In-Degree Topological Sort.

## Components
- `AI/three_d_parallelism_orchestrator.py`: 3D Cartesian coordinates, NVLink intra-node TP grouping, and InfiniBand DP/PP process groups.
- `DSA/TopologicalSortKahnsAlgo.java`: $O(V + E)$ Kahn's BFS algorithm with in-degree array and cycle detection.
- `Interview/technical_questions.md`: Sizing 405B model parallelism dimensions and Kahn's cycle detection proof.
- `Notes/notes.md`: Process group communicators and iterative queue safety.
