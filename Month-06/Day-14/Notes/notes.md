# Engineering Notes — Day 14: Turn-Taking & Tree Construction Math

## 1. Turn-Taking State Machine Invariants
- Speech Onset: $\Delta t_{\text{speech}} \ge T_{\text{start}}$ (prevents transient acoustic clicks from opening sessions).
- Endpoint Handover: $\Delta t_{\text{silence}} \ge T_{\text{endpoint}}$ (signals turn completion to downstream LLM).

## 2. Binary Tree Index Partitioning
For Preorder `[root | left_subtree | right_subtree]` and Inorder `[left_subtree | root | right_subtree]`:
- Left subtree preorder bounds: `[preStart + 1, preStart + numsLeft]`
- Right subtree preorder bounds: `[preStart + numsLeft + 1, preEnd]`
