# 🎯 Technical Interview Questions — Day 20: Citation Audits & Fenwick Trees

## Question 1: How do you mathematically define Citation Precision and Citation Recall in a RAG system?
**Answer:**
- **Citation Precision:**
  $$\text{Precision} = \frac{\text{Number of citations accurately supporting the asserted claim}}{\text{Total citations emitted by the LLM}}$$
  Low precision indicates hallucinated or irrelevant citations where the model asserts a fact and links to an unrelated document.
- **Citation Recall:**
  $$\text{Recall} = \frac{\text{Number of verifiable factual claims accompanied by citations}}{\text{Total factual claims made in the response}}$$
  Low recall indicates unbacked assertions where claims derived from retrieved knowledge lack provenance tags.

---

## Question 2: How does a Fenwick Tree (Binary Indexed Tree) perform point updates and prefix sums in O(log N)?
**Answer:**
- **Bitwise Navigation:** A Fenwick tree relies on the least significant bit (LSB) formula `i & (-i)`.
  - In two's complement, `-i = (~i) + 1`. Bitwise AND with `i` extracts the lowest set bit representing the range length managed by index `i`.
- **Query Operation:** To compute prefix sum `sum(1..i)`, repeatedly add `tree[i]` and strip the lowest set bit: `i -= i & (-i)`. This takes at most $\log_2 N$ steps.
- **Update Operation:** To update index `i` with delta, add delta to `tree[i]` and advance to parent ranges by adding the lowest set bit: `i += i & (-i)`. This also takes at most $\log_2 N$ steps.
