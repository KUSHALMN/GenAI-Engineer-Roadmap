# Day 07: Technical Interview Preparation — Parameter Freezing & Java Immutability

### Q1: Why does adapter-based fine-tuning (LoRA) prevent catastrophic forgetting better than full fine-tuning?
**Answer:**
Full fine-tuning updates all $W$ matrices with non-zero gradients across billions of parameters, altering the pretrained representation manifolds. LoRA freezes $W_0$ completely and only optimizes a tiny additive low-rank delta $\Delta W = B \cdot A$. The core foundational knowledge remains mathematically intact in the frozen weights.

### Q2: What are the requirements to make a Java class completely immutable?
**Answer:**
1. Declare the class `final` so subclasses cannot override methods to introduce mutable state.
2. Make all fields `private` and `final`.
3. Do not provide any setter methods.
4. If fields refer to mutable objects (e.g. `List`, `Date`), make defensive copies in constructors and return unmodifiable views or new copies in getters.
