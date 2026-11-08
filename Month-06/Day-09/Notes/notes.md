# Engineering Notes — Day 09: Audio Pipeline & Floyd's Cycle Proof

## 1. Short-Time Energy & Zero-Crossing Rate
- **Short-Time Energy (STE):**
  $$E_n = \frac{1}{N} \sum_{m=0}^{N-1} x^2[m]$$
  High during voiced vowel phonemes.
- **Zero-Crossing Rate (ZCR):**
  $$Z_n = \frac{1}{2(N-1)} \sum_{m=1}^{N-1} |\text{sgn}(x[m]) - \text{sgn}(x[m-1])|$$
  High during unvoiced fricatives ('s', 'sh', 'f').

## 2. Fast/Slow Pointer Invariant
- Phase 1: `slow = slow.next; fast = fast.next.next;` Detects loop existence in $O(N)$ time, $O(1)$ space.
- Phase 2: `ptr1 = head; ptr2 = slow;` Steps at rate 1 to pinpoint cycle origin.
