# 📅 Day 16 — All-to-All Collective Primitives & Sliding Window Maximum

## Overview
Modeling collective communication primitives (All-Reduce vs All-to-All) across NVLink and InfiniBand interconnects alongside solving LeetCode 239 (Sliding Window Maximum) using an $O(N)$ monotonic deque.

## Components
- `AI/collective_communication_topology.py`: All-Reduce, All-to-All, and P2P communication latency and bandwidth modeling.
- `DSA/SlidingWindowMaximumTimedSet.java`: $O(N)$ monotonic deque algorithm for sliding window peak extraction.
- `Interview/technical_questions.md`: MoE All-to-All bisection bandwidth bottlenecks and deque amortized analysis.
- `Notes/notes.md`: Interconnect latency math and index-based deque invariants.
