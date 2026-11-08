# Technical Interview Preparation — Audio Processing & Fast/Slow Pointers

## 1. Why 16kHz Mono PCM is the Standard for Speech AI
**Question:** Why do automatic speech recognition (ASR) models like Whisper, Conformer, and wav2vec operate on 16kHz mono audio rather than 44.1kHz stereo audio?

**Answer:**
- **Nyquist-Shannon Sampling Theorem:**
  - A sampling rate $f_s$ can capture frequencies up to the Nyquist frequency $f_N = f_s / 2$.
  - At 16kHz, frequencies up to 8,000 Hz are accurately reproduced.
  - Human speech intelligibility (formants $F_1, F_2, F_3$ and consonant fricatives) resides predominantly between 300 Hz and 7,500 Hz. Higher frequencies convey acoustic timbre/music fidelity, not linguistic content.
- **Compute and Memory Economics:**
  - Downsampling from 44.1kHz stereo (2 channels) to 16kHz mono (1 channel) yields a $(44100 \times 2) / (16000 \times 1) \approx 5.51\times$ reduction in data volume.
  - Reduces FFT frame count and linearizes transformer self-attention sequences in the audio encoder.

---

## 2. Floyd's Cycle Detection Mathematical Proof
**Question:** Prove that in Floyd's Cycle Finding Algorithm (LC 142), moving one pointer to `head` and stepping both pointers at speed 1 meets precisely at the cycle entrance.

**Answer:**
- Let $L$ be the distance from `head` to the cycle entry.
- Let $C$ be the circumference of the cycle.
- Let $d$ be the distance from the cycle entry to the meeting point.
- When `slow` and `fast` meet:
  - Distance traveled by `slow`: $D_s = L + d$.
  - Distance traveled by `fast`: $D_f = L + d + nC$ where $n \ge 1$ is complete loops.
- Because `fast` moves at $2\times$ the speed of `slow`:
  $$D_f = 2 D_s \implies L + d + nC = 2(L + d) \implies L + d = nC \implies L = nC - d = (n-1)C + (C - d)$$
- Notice that $(C - d)$ is the remaining distance from the meeting point to the cycle entry!
- Therefore, if one pointer starts at `head` (traveling $L$) and the other starts at the meeting point (traveling $(n-1)C + (C-d)$), they will both arrive at the cycle entry after exactly $L$ steps.
