# 📅 Day 09 — FlashAttention Tiled Softmax & KMP String Matching

## Overview
Simulating FlashAttention-1/2 block tiling and the Online Softmax rescaling algorithm alongside implementing the Knuth-Morris-Pratt (KMP) string search algorithm (LeetCode 28).

## Components
- `AI/flash_attention_simulator.py`: SRAM block tiling ($B_r \times B_c$), running row maximum $m_i$, and $O(N)$ HBM attention.
- `DSA/KmpStringMatching.java`: $O(N + M)$ linear string matching with precomputed LPS array.
- `Interview/technical_questions.md`: GPU memory hierarchy roofline analysis and KMP non-backtracking proofs.
- `Notes/notes.md`: Online softmax mathematical rescaling and KMP invariants.
