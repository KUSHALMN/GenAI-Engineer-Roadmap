# Technical Interview Preparation — Multimodal Architecture & Sorting

## 1. Early Fusion vs. Late Fusion in Multimodal LLMs
**Question:** Compare early fusion, late fusion, and cross-attention architectures in Multimodal Large Language Models (MLLMs).

**Answer:**
- **Early Fusion (Token Interleaving):** Non-text modalities are projected into LLM token space and interleaved with text. Deep cross-attention across all layers, but scales as $O((N_{text} + N_{vis})^2)$ in memory and compute.
- **Late Fusion:** Unimodal encoders process each stream separately and pool vectors at the final classification or projection layer. Low compute cost, but lacks fine-grained inter-modal reasoning.
- **Perceiver / Cross-Attention:** Uses learned queries to compress large visual patch sequences into fixed tokens (e.g. 64 or 128 tokens) passed into cross-attention layers.

## 2. QuickSort Partition Algorithms
**Question:** Why does Lomuto partition degrade on arrays with many duplicate keys, and how does Dutch National Flag (3-way) solve it?

**Answer:**
- Lomuto places equal elements on one side, leading to an unbalanced $O(N^2)$ recursion.
- 3-Way Partition maintains three regions ($< pivot$, $== pivot$, $> pivot$), isolating all equal keys in $O(N)$ single-pass and recursing only on strictly smaller and greater elements.
