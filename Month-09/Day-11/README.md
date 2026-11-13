# 📅 Day 11 — Mixture of Experts (MoE) Routing & Edit Distance DP

## Overview
Simulating Mixture-of-Experts (MoE) Top-2 gating with capacity factor bounds and load balancing auxiliary loss alongside mastering LeetCode 72 (Edit Distance) with $O(\min(M, N))$ space-optimized DP.

## Components
- `AI/moe_expert_router.py`: Top-K gating router, capacity factor enforcement, dropped token handling, and Switch Transformer auxiliary loss.
- `DSA/EditDistanceTimedSet.java`: $O(M \cdot N)$ time, $O(\min(M, N))$ space dynamic programming string alignment.
- `Interview/technical_questions.md`: MoE sparse activation mechanics and DP space optimization derivations.
- `Notes/notes.md`: Capacity factor trade-offs and Top-2 weight normalization rules.
