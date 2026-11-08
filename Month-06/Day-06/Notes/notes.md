# Engineering Notes — Day 06: Chart QA & Two Pointers Convergence

## 1. Chart Decomposition Schema
- Chart type detection $\rightarrow$ Axis calibration (pixel-to-value ratio) $\rightarrow$ Series point extraction $\rightarrow$ Summary generation.

## 2. Two Pointers Invariants
- **3Sum:** Sort array first $O(N \log N)$. For fixed $i$, move `left` and `right`. Skip duplicate values to avoid duplicate triplets.
- **Trapping Rain Water:** Move inward from lower boundary bar; water height is determined strictly by the lower of `leftMax` and `rightMax`.
