# Interview Questions: Multilingual Search & Fenwick Trees

### Q1: How do multilingual embedding models align representations across languages without manual translation?
**Answer**:
Multilingual models use **Parallel Translation Mining** and **Contrastive Cross-Lingual Objectives** (e.g. InfoNCE). During pre-training, translated sentence pairs $(s_{\text{en}}, s_{\text{es}})$ are presented in the same batch. The contrastive loss forces $E(s_{\text{en}})$ and $E(s_{\text{es}})$ to have a high cosine dot product while pushing random sentences in other languages apart, yielding language-invariant semantic geometries.

### Q2: Why does the Fenwick Tree use `i & (-i)` to navigate nodes?
**Answer**:
In two's complement binary representation, `-i` is formed by flipping all bits of `i` and adding `1`.
Bitwise AND `i & (-i)` isolates the **lowest set bit (LSB)** of `i`.
- In a Fenwick Tree, adding the LSB (`i += (i & -i)`) ascends to the next interval responsible for updating values in the BIT hierarchy.
- Subtracting the LSB (`i -= (i & -i)`) descends through disjoint sub-ranges to accumulate the prefix sum.

### Q3: How does Fenwick Tree compare to a Segment Tree?
**Answer**:
- **Fenwick Tree**:
  - Smaller constant factors, half the memory ($\mathcal{O}(N)$ vs $\mathcal{O}(4N)$).
  - Implementation is extremely compact (~15 lines of code).
  - Best for prefix sums and point updates with invertible operations (addition, XOR).
- **Segment Tree**:
  - More versatile: handles non-invertible range operations (Range Minimum Query, Range GCD) and range updates with Lazy Propagation.
