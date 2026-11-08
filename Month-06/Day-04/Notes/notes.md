# Engineering Notes — Day 04: Document Layout Understanding & Radix Sorting

## 1. Bounding Box Geometry & Overlap Invariants
- Bounding Box representation: $(x_1, y_1, x_2, y_2)$ where $(x_1, y_1)$ is top-left, $(x_2, y_2)$ is bottom-right.
- Intersection over Union (IoU):
  $$\text{IoU}(A, B) = \frac{\text{Area}(A \cap B)}{\text{Area}(A \cup B)}$$
- Two-column separation gutter:
  $$\text{Gutter} = [x_{1, \text{col2}} - x_{2, \text{col1}}]$$

## 2. Radix Sort Stability Requirement
Radix Sort requires the inner digit sort to be **strictly stable**. If the digit sort were unstable, sorting higher-order digits would destroy the sorted invariant previously established by lower-order digits.
