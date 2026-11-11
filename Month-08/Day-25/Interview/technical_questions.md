# 🎯 Technical Interview Questions — Day 25: Multi-Region Residency & Hard DSA Mock B

## Question 1: How do you architect data residency compliance across EU, US, and APAC for LLM inference?
**Answer:**
1. **Edge Ingress Geofencing:** Cloudflare Workers or Envoy Gateways inspect the client's source IP, DNS geolocation, and tenant residency contractual requirements.
2. **Dedicated Sovereign VPCs:** Isolated clusters deployed in `eu-central-1` (Frankfurt) ensure prompt tokens, embeddings, and vector indices never leave European borders, guaranteeing full GDPR Article 44–50 compliance.
3. **Decoupled Model Weights vs User Context:** Pre-trained model weights are universal, but all runtime caches, KV state, vector databases, and audit logs are pinned to local KMS-encrypted regional volumes.

---

## Question 2: In LeetCode 312 (Burst Balloons), why does working "from the last balloon burst" make interval DP work?
**Answer:**
- If we consider the *first* balloon burst, the subproblems become dependent because bursting balloon $k$ causes balloon $k-1$ and $k+1$ to become adjacent, dynamically altering subsequent boundary multipliers.
- **Reversed Subproblem Thinking:** If we instead choose balloon $k$ as the *last* balloon to burst in interval $[left, right]$, the boundary balloons ($left - 1$ and $right + 1$) remain intact until the very end.
- Thus, the subproblems $[left, k-1]$ and $[k+1, right]$ become completely independent, enabling classical $O(N^3)$ interval dynamic programming:
  $$DP[left][right] = \max_{k} \{ DP[left][k-1] + DP[k+1][right] + arr[left-1] \cdot arr[k] \cdot arr[right+1] \}$$
