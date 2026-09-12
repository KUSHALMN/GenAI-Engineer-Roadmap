# Day 34 (Month 02 - Day 02): Coding Interview Questions
## Focus: Dynamic Programming — Climbing Stairs (LC 70)

---

### Q1: Derive the Climbing Stairs recurrence and explain why it's Fibonacci.

**Answer:**
- **State**: `dp[i]` = number of distinct ways to reach step `i`
- **Choice**: From step `i`, you arrived from either `i-1` (took 1 step) or `i-2` (took 2 steps)
- **Recurrence**: `dp[i] = dp[i-1] + dp[i-2]`
- **Base cases**: `dp[1] = 1`, `dp[2] = 2`
- **Fibonacci connection**: This is exactly Fibonacci shifted by 1 — `climbStairs(n) = fib(n+1)`

**Trace** — n=5:
```
dp[1]=1, dp[2]=2, dp[3]=3, dp[4]=5, dp[5]=8
```
Space-optimized to O(1) using two variables `prev2`, `prev1`.

---

### Q2: How do you extend Climbing Stairs to k steps (generalized)?

**Answer:**
```java
int[] dp = new int[n + 1];
dp[0] = 1;
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= k && j <= i; j++)
        dp[i] += dp[i - j];
```
- **Time**: O(n × k), **Space**: O(n)
- For k=2 this reduces to the standard Fibonacci solution.
- For k=n (can jump any number of steps): `dp[i] = 2^(i-1)` — each step is either included or not.

---

### Q3: What DP problems reduce to Climbing Stairs?

**Answer:**
| Problem | Reduction |
|---------|-----------|
| LC 746 Min Cost Climbing Stairs | Same recurrence + cost array |
| LC 91 Decode Ways | `dp[i] = dp[i-1] + dp[i-2]` with validity checks |
| LC 509 Fibonacci Number | Direct Fibonacci |
| LC 1137 Tribonacci | 3-step variant |

**LC 746 extension**:
```java
dp[i] = Math.min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]);
```
