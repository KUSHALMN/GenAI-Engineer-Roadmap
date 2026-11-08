# Engineering Notes — Day 05: Table Extraction & Binary Search Invariants

## 1. Semi-Structured Table Parsing Invariants
- **Row/Col Span Normalization:** When cell $(r, c)$ has $\text{rowspan}=2$, cell $(r+1, c)$ must be shifted right or populated with a pointer to prevent column misalignment.
- **Numeric Validation Invariant:**
  $$\sum_{j=1}^{C-1} \text{Cell}[i, j] = \text{Cell}[i, C] \quad \forall i \in [1, R]$$

## 2. Binary Search Invariant Template
```
1. Target search: low <= high; mid = low + (high - low)/2
2. Peak search: low < high; compare mid and mid + 1
3. Rotated array: identify which half is monotonically sorted before choosing direction
```
