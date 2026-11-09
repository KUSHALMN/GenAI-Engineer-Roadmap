# Engineering Notes — Day 15: Speech-to-Speech & Heap Invariants

## 1. Latency Budget for Conversational AI
- Total human conversational reaction time: $\approx 200 - 300$ ms.
- Budget: VAD detection ($120$ ms) + Model inference ($100$ ms) + Audio decoding ($30$ ms).

## 2. PriorityQueue Space Invariant
- Min-Heap maintaining $K$ elements: Space is strictly $O(K)$.
