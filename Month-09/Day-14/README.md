# 📅 Day 14 — FP8/BF16 Mixed Precision & Histogram Monotonic Stack

## Overview
Analyzing FP32, FP16, BF16, and FP8 (E4M3 vs E5M2) numerical formats, dynamic loss scaling, and gradient clipping alongside solving LeetCode 84 (Largest Rectangle in Histogram) using a monotonic stack.

## Components
- `AI/mixed_precision_numerical_stability.py`: Floating point bit layouts, dynamic loss scaler with underflow/overflow recovery.
- `DSA/LargestRectangleHistogramTimedSet.java`: $O(N)$ monotonic stack algorithm with virtual sentinel bar.
- `Interview/technical_questions.md`: BF16 exponent advantage and Monotonic Stack $2N$ amortized proof.
- `Notes/notes.md`: Gradient norm clipping mathematics and histogram width boundary formulas.
