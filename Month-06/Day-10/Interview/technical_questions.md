# Technical Interview Preparation — Speech-to-Text & Advanced Linked Lists

## 1. Handling Hallucinations in Whisper on Silence & Acoustic Noise
**Question:** Why do autoregressive speech-to-text models like Whisper hallucinate repetitive strings (e.g., "Thank you for watching!", "Subtitles by...") during silent audio segments, and how is this mitigated in production?

**Answer:**
- **Why Hallucinations Occur:**
  - Whisper's text decoder is a causal language model conditioned on cross-attention audio encoder states.
  - When the audio is silent or pure ambient noise, the encoder outputs low-magnitude vectors near zero.
  - The decoder's language model prior dominates, generating common concluding subtitle phrases present in the training set (e.g. YouTube video end screens).
  - Repetition loops occur because autoregressive decoders reinforce their own output history.
- **Production Mitigation Strategy:**
  1. *Voice Activity Detection (VAD) Pre-Filtering:* Never send silent frames to the ASR model. Strip silence at the frontend.
  2. *No-Speech Probability Threshold:* Whisper outputs a `no_speech_prob` metric. If $> 0.6$, reject output.
  3. *Temperature Fallback:* If repetition penalty or compression ratio fails thresholds, re-decode with higher temperature ($T \in [0.2, 0.4, 0.8]$).

---

## 2. Reverse Nodes in k-Group (LC 25) Invariants
**Question:** Explain how to reverse nodes in $k$-group with strictly $O(1)$ auxiliary space without corrupting pointers when the final segment contains fewer than $k$ nodes.

**Answer:**
1. **Lookahead Check:** Count ahead $k$ nodes from `curr`. If fewer than $k$ nodes exist before reaching `null`, immediately return the unchanged `head`.
2. **Reversal Subroutine:** Reverse exactly $k$ pointers in-place using standard 3-pointer reversal (`prev`, `curr`, `next`).
3. **Recursive or Iterative Connection:**
   - After reversing $k$ nodes, the original `head` becomes the tail of the reversed group.
   - Attach `head.next` to the result of recursing on the remaining list starting at the $(k+1)$-th node.
