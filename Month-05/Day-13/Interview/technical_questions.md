# Day 13: Technical Interview Preparation — Catastrophic Forgetting & RandomizedSet

### Q1: What is "Catastrophic Forgetting" and how can it be mitigated during domain fine-tuning?
**Answer:**
Catastrophic forgetting occurs when fine-tuning a model on a narrow domain causes it to abruptly lose its generalized capabilities (e.g. coding or arithmetic).
*Mitigations:*
1. **Replay Buffer (Data Mixing):** Mix in 5-10% general instruction data (e.g. OpenHermes or general QA) with domain data.
2. **LoRA / PEFT:** Adapters keep original base weights frozen.
3. **KL Divergence Regularization:** Penalize large output logit shifts relative to the original base model.

### Q2: Why is the swap-with-last trick mandatory for $O(1)$ removal in an `ArrayList`?
**Answer:**
Deleting from an arbitrary index in an array takes $O(n)$ because all subsequent elements must be shifted left. Swapping the target element with the last element and calling `list.remove(list.size() - 1)` takes $O(1)$ because no other elements require shifting.
