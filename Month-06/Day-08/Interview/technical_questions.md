# Technical Interview Preparation — Multimodal RAG & Prefix Sums

## 1. Provenance Attribution in Multimodal RAG
**Question:** How do you guarantee source attribution and citations when an answer combines unstructured text, visual tables, and page screenshots?

**Answer:**
1. **Unified Evidence Metadata Schema:** Every retrieved chunk carries `doc_id`, `page_number`, `modality` (`text`, `table`, `image`), and a spatial bounding box `bbox = (x1, y1, x2, y2)`.
2. **Context Interleaving:** The context prompt explicitly labels modality boundaries:
   `[EVIDENCE-1: Text, Doc A, Page 4] ... [EVIDENCE-2: Table, Doc A, Page 4] ... [EVIDENCE-3: Image crop, Doc B, Page 1]`.
3. **Citation Verifier:** Post-generation regex ensures every claim cites its matching evidence ID. If a claim references numbers found only in Evidence-2 (Table), but fails to cite Evidence-2, the output is flagged for grounding hallucination.

---

## 2. Prefix Sum Modulo: Continuous Subarray Sum (LC 523) Invariant
**Question:** Why does storing the earliest index of `prefixSum % k` in a HashMap find a continuous subarray with sum divisible by $k$?

**Answer:**
- Let $S[i]$ be the prefix sum up to index $i$.
- The sum of subarray from $j+1$ to $i$ is $S[i] - S[j]$.
- For $(S[i] - S[j])$ to be divisible by $k$:
  $$(S[i] - S[j]) \equiv 0 \pmod k \iff S[i] \equiv S[j] \pmod k$$
- Therefore, if we encounter the same remainder at index $i$ that previously occurred at index $j$, the subarray between them is divisible by $k$.
- Storing only the **first** occurrence index maximizes $(i - j)$ to ensure length $\ge 2$.
