# 🎯 Technical Interview Questions — Day 26: Model Upgrades & LRU Cache

## Question 1: How do you safely migrate a Tier-1 production service from an older foundation model to a newer version without breaking downstream schemas?
**Answer:**
1. **Shadow Traffic (Dark Launch):** 100% of live production prompts are asynchronously duplicated to the candidate model. Outputs are compared using automated regression evaluators (BLEU, semantic similarity, JSON schema validation).
2. **Canary Phasing (5% -> 20% -> 50% -> 100%):** Traffic is split via deterministic user ID hashing. Real-time dashboards monitor exception rates, user feedback, and latency metrics.
3. **Automated Rollback Circuit Breakers:** If the canary error rate spikes by $> 0.5\%$ or latency violates P99 SLOs, the traffic router automatically reverts to the legacy model in $< 100\text{ms}$.
4. **Graceful Sunsetting:** The legacy model endpoint is placed in deprecated mode with warning headers, then soft-retired before final decommissioning.

---

## Question 2: Why does an LRU Cache require both a Doubly Linked List and a Hash Map to achieve O(1) time?
**Answer:**
- A Hash Map provides $O(1)$ average time key-to-node lookups, but does not inherently maintain access order.
- A Singly Linked List allows $O(1)$ insertion at head, but deleting an arbitrary node requires finding its predecessor, which takes $O(N)$ time.
- A **Doubly Linked List** allows any node to be removed in $O(1)$ time because `node.prev` and `node.next` are directly accessible without traversal.
- Combining a Hash Map with a Doubly Linked List achieves true $O(1)$ worst-case/amortized time for both `get` and `put`.
