# 🎯 Day 03 (Month 03) Technical Interview Questions & Answers

## 1. How do Vision-Language Models (VLMs like LLaVA or GPT-4o) process images alongside textual tokens?
**Answer:**
1. **Patch Projection**: An image is split into a grid of non-overlapping patches (e.g. $14 \times 14$ pixels in ViT / CLIP).
2. **Visual Encoder**: A pretrained Vision Transformer processes these patches into visual token feature vectors.
3. **Multimodal Projector (Linear or Q-Former / Cross-Attention)**: A projection layer maps visual embeddings into the identical dimensional embedding space as the text tokenizer.
4. **Unified Autoregressive Decoding**: Visual tokens are prepended or interleaved with textual prompt tokens and passed through standard Transformer decoder attention layers. The LLM attends seamlessly across words and image patches.

---

## 2. What are the key bottlenecks in Multimodal RAG pipelines?
**Answer:**
- **Vector Index Explosion**: Cross-modal embeddings (e.g. CLIP ViT-B/32 or SigLIP) have high dimensionality ($512-1024$), and document images consume far more storage than raw text.
- **Visual Token Context Cost**: A single high-resolution image consumes between 256 to 1,600 LLM context tokens, consuming token budgets rapidly.
- **OCR vs Native VLM Trade-off**: Pure OCR loses tabular coordinates, flowcharts, and colors. Native VLMs capture visuals but can hallucinate tiny numerical digits in dense spreadsheets. Best practice: Hybrid OCR text extraction combined with thumbnail visual grounding.

---

## 3. Explain how Dynamic Programming on Trees solves House Robber III (LC 337) in $O(N)$ time.
**Answer:**
A naive recursive solution exhibits overlapping subproblems of exponential $O(2^N)$ time.
In Tree DP:
- Define a post-order traversal function returning a 2-element array `[rob, notRob]` for each subtree root:
  - `rob`: Maximum money stolen from this subtree if we *do* rob the root. Invariant: We cannot rob its left and right children $\implies$ $val + left[notRob] + right[notRob]$.
  - `notRob`: Maximum money stolen if we *do not* rob the root. Invariant: We are free to either rob or not rob each child $\implies$ $\max(left[rob], left[notRob]) + \max(right[rob], right[notRob])$.
Each node in the tree is visited exactly once, yielding strict $O(N)$ time and $O(H)$ recursion space.
