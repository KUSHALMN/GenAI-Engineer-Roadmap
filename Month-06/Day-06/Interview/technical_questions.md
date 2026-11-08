# Technical Interview Preparation — Chart QA & Two Pointers

## 1. Grounding in Chart QA: Separating Observed Facts from Inferences
**Question:** In vision-language pipelines for chart analysis, why is it critical to separate observed facts from inferred explanations, and how do you design prompt constraints for it?

**Answer:**
- **Observed Facts:** Direct measurements verifiable from visual pixel data (e.g. "Bar A height is 150 units, Bar B height is 300 units; Bar B is 2x Bar A").
- **Inferred Explanations:** Hypotheses regarding *why* the data exhibits that trend (e.g. "Revenue grew due to marketing campaigns").
- **Risks:** Unconstrained LLMs frequently blur these categories, hallucinating causal real-world justifications that are absent from the image.
- **Architectural Solution:** Dual-field JSON schema (`observed_facts: List[str]`, `inferred_explanations: List[str]`). The validation layer rejects outputs where quantitative claims lack grounded axis measurements.

---

## 2. Trapping Rain Water: $O(1)$ Space Invariant Proof
**Question:** Explain why the two-pointer approach for Trapping Rain Water achieves $O(1)$ auxiliary space without needing precomputed prefix/suffix arrays.

**Answer:**
- Water trapped at index $i$ depends on $\min(\text{leftMax}[i], \text{rightMax}[i]) - \text{height}[i]$.
- In two pointers, if `height[left] <= height[right]`:
  - We know for certain that `leftMax <= height[right] <= rightMax`.
  - Therefore, the water trapped at `left` is strictly bounded by `leftMax`, regardless of any taller bars further to the right!
  - We can safely compute `total += leftMax - height[left]` and advance `left++`.
  - Symmetrically, if `height[right] < height[left]`, trapped water is bounded by `rightMax`.
