# Day 14: Technical Interview Preparation — DPO vs RLHF & TimeMap

### Q1: Why does Direct Preference Optimization (DPO) simplify RLHF?
**Answer:**
Traditional RLHF requires training an explicit Reward Model, followed by unstable Reinforcement Learning (PPO) involving four concurrent models (actor, critic, reference, reward). DPO analytically proves that the optimal policy under the Bradley-Terry preference model can be derived directly from preference pairs using a closed-form cross-entropy loss, eliminating the reward model and PPO training loop.

### Q2: Why is Binary Search suitable for TimeMap retrieval?
**Answer:**
Calls to `set(key, value, timestamp)` arrive with strictly increasing timestamps. Therefore, the list of entries for each key is inherently sorted by timestamp, allowing binary search to locate the floor timestamp in $O(\log N)$ time.
