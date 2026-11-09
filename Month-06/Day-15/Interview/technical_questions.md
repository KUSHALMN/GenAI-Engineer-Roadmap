# Technical Interview Preparation — Speech-to-Speech & Heap Patterns

## 1. Cascaded (ASR -> LLM -> TTS) vs. Native Audio-to-Audio (GPT-4o Audio / Gemini Live)
**Question:** Analyze the trade-offs between cascaded voice systems and native speech-to-speech models across latency, safety, and acoustic expressiveness.

**Answer:**
| Dimension | Cascaded (ASR $\rightarrow$ LLM $\rightarrow$ TTS) | Native Speech-to-Speech |
|:---|:---|:---|
| **Time-to-First-Audio (TTFA)** | $500 - 900$ ms (ASR delay + LLM first sentence + TTS) | $200 - 300$ ms (Streamed audio token-to-token) |
| **Paralinguistics** | Completely lost: transcript strips pitch, sighs, laughing, whispering | Preserved natively: can laugh, sing, whisper, and mimic accent |
| **Observability & Safety** | Extremely high: text prompt guardrails and filters inspect every token | Low/Challenging: difficult to inspect audio tokens for subtle injections |
| **Component Upgradability**| Modular: swap LLaMA-3 for Claude or Whisper for Conformer | Monolithic: entire model must be retrained end-to-end |

---

## 2. Merge K Sorted Lists: PriorityQueue Invariant
**Question:** Why does using a Min-Heap of size $K$ merge $K$ sorted lists of total $N$ elements in $O(N \log K)$ time rather than $O(N \log N)$?

**Answer:**
- At any moment, the Min-Heap contains at most one candidate node from each of the $K$ lists.
- Therefore, the heap size is strictly bounded by $K$ (not $N$).
- For each of the $N$ total elements:
  - Extract min: $O(\log K)$.
  - Insert next node from the same list: $O(\log K)$.
- Total time: $N \times 2 \log K = O(N \log K)$.
- When $K \ll N$ (e.g. merging 10 lists of 100,000 items each), $O(N \log K)$ is dramatically faster than sorting all items $O(N \log N)$.
