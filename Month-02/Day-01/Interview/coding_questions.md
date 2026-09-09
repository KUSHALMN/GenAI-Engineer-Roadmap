# Day 32 (Month 02 - Day 01): Coding Interview Questions
## Focus: Dynamic Programming — Coin Change (LC 322)

---

### Q1: Why is greedy incorrect for Coin Change and when does it work?

**Answer:**
- **Greedy failure**: With coins `[1, 5, 6, 9]` and amount `11`, greedy picks `9 → 1 → 1` = 3 coins. Optimal is `5 + 6` = 2 coins.
- **Greedy works** only when the coin system is **canonical** (e.g., standard US currency: 25, 10, 5, 1). Canonical systems have the property that the greedy choice never leads to a suboptimal global solution.
- **Proof of failure**: Greedy lacks the **optimal substructure** guarantee for arbitrary coin sets — a locally optimal choice (largest coin ≤ amount) can block a globally optimal path.

---

### Q2: Walk through the DP recurrence for Coin Change.

**Answer:**
```
dp[0] = 0                          // base: 0 coins to make amount 0
dp[i] = min(dp[i - coin] + 1)      // for each coin where coin <= i
dp[i] = amount + 1 initially       // sentinel for "impossible"
```

**Trace** — coins `[1, 2, 5]`, amount `6`:
```
dp[0]=0, dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=2, dp[5]=1, dp[6]=2
```
- `dp[6]`: try coin=1 → dp[5]+1=2, coin=2 → dp[4]+1=3, coin=5 → dp[1]+1=2 → min=2 ✅

**Time**: O(amount × |coins|)
**Space**: O(amount)

---

### Q3: How would you reconstruct which coins were used (not just the count)?

**Answer:**
Track a `parent[]` array alongside `dp[]`:
```java
int[] parent = new int[amount + 1];
Arrays.fill(parent, -1);

for (int i = 1; i <= amount; i++) {
    for (int coin : coins) {
        if (coin <= i && dp[i - coin] + 1 < dp[i]) {
            dp[i] = dp[i - coin] + 1;
            parent[i] = coin;   // record which coin was used
        }
    }
}

// Reconstruct
List<Integer> path = new ArrayList<>();
int cur = amount;
while (cur > 0) {
    path.add(parent[cur]);
    cur -= parent[cur];
}
```
**Time/Space**: O(amount) extra for `parent[]`.

---

### Q4: What is the unbounded knapsack connection?

**Answer:**
Coin Change is a special case of **unbounded knapsack**:
- **Unbounded**: Each coin can be used unlimited times (vs. 0/1 knapsack where each item is used once).
- **Knapsack framing**: Items = coins (weight = value = denomination), capacity = amount, minimize item count instead of maximizing value.
- The inner loop iterates over all coins for each amount `i` — this naturally allows reuse because we read from `dp[i - coin]` which was already updated in the current pass (forward DP, not backward like 0/1 knapsack).
