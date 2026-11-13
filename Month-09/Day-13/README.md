# 📅 Day 13 — RingAttention Context Parallelism & Longest Valid Parentheses

## Overview
Simulating Context Parallelism via RingAttention circular KV transmission and Online Softmax rescaling alongside solving LeetCode 32 (Longest Valid Parentheses) via Stack and $O(1)$ Space Two-Pass algorithms.

## Components
- `AI/ring_attention_simulator.py`: Distributed circular shift communication, P2P non-blocking overlap, and online softmax updates.
- `DSA/LongestValidParenthesesTimedSet.java`: $O(N)$ stack and $O(1)$ space two-pass bidirectional scans.
- `Interview/technical_questions.md`: Million-token context scaling proofs and bidirectional scan necessity.
- `Notes/notes.md`: Context Parallelism vs Tensor Parallelism and stack sentinel initialization.
