# Engineering Notes — Day 10: Speech-to-Text & Linked List Reversal

## 1. Word-Level Alignment (Cross-Attention Timestamps)
- Cross-attention weights between decoder token positions and encoder audio frame frames ($50$ frames/sec) reveal where the acoustic evidence for each word begins and ends.
- Dynamic Time Warping (DTW) on cross-attention heatmaps yields millisecond-accurate word boundaries.

## 2. Linked List Invariants
- **Reorder List:** Find midpoint $\rightarrow$ Reverse right half $\rightarrow$ Interleave node-by-node.
- **k-Group Reversal:** Preserve connection across group boundaries: `tail_of_prev_group.next = head_of_current_reversed_group`.
