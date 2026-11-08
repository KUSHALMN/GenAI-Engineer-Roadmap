# Technical Interview Preparation — Multimodal Embeddings & Sliding Window

## 1. CLIP Contrastive Loss & Modality Gap
**Question:** Explain the dual-encoder CLIP architecture, the InfoNCE contrastive loss objective, and the phenomenon known as the "modality gap".

**Answer:**
- **Dual-Encoder Architecture:**
  - An image encoder $f_{\theta}(I)$ and a text encoder $g_{\phi}(T)$ independently project inputs into an identical $D$-dimensional normalized vector space.
- **InfoNCE Loss:**
  - For a batch of $N$ image-text pairs $(I_i, T_i)$:
  $$\mathcal{L}_{i} = -\log \frac{\exp(\text{sim}(I_i, T_i) / \tau)}{\sum_{j=1}^N \exp(\text{sim}(I_i, T_j) / \tau)}$$
  - Maximizes cosine similarity of positive pairs while pushing away $N-1$ negative pairs.
- **Modality Gap:**
  - In practice, learned image embeddings and text embeddings occupy two disjoint geometric clusters in the shared hypersphere.
  - Caused by cone effect of contrastive optimization with temperature parameter $\tau$. Cross-modal cosine similarities are systematically shifted lower than intra-modal similarities.

---

## 2. Sliding Window: Minimum Window Substring Frequency Invariant
**Question:** How does the `formed == required` variable optimize Minimum Window Substring (LC 76) from $O(26 \cdot N)$ to strictly $O(N)$?

**Answer:**
- A naive check verifies whether all 26/128 characters in `windowCount` meet `targetCount` on each step, requiring $O(|\Sigma|)$ work per iteration.
- By tracking `formed` (the count of distinct characters whose window frequency matches or exceeds the required frequency):
  - When `windowCount[c] == targetCount[c]`, increment `formed++`.
  - When shrinking from the left, if `windowCount[c] < targetCount[c]`, decrement `formed--`.
  - Checking `formed == required` is an $O(1)$ integer equality check, guaranteeing strict $O(N)$ amortized time.
