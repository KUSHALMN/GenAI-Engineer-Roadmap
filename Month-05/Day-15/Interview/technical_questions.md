# Day 15: Technical Interview Preparation — Knowledge Distillation & Hit Counter

### Q1: Why do soft targets from a teacher model contain more information than hard ground-truth labels?
**Answer:**
Hard one-hot labels only indicate the correct class (e.g., `[1, 0, 0]`). Teacher soft probabilities contain the "dark knowledge" of relative semantic similarities between incorrect classes (e.g., `[0.70, 0.28, 0.02]`), teaching the student that class B is much closer to class A than class C.

### Q2: Why is the circular bucket array superior to a Queue for the Hit Counter in production?
**Answer:**
A Queue stores every individual hit timestamp, growing without bound ($O(H)$ space) under high traffic spikes (e.g. 100,000 requests/sec). A circular bucket array of size 300 uses strict $O(1)$ constant memory and zero dynamic allocations regardless of request volume.
