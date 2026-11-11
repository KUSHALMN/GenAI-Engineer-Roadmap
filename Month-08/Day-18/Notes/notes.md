# 📝 Notes — Day 18: Content Policy Engine & Advanced DP

- **Policy Hierarchy:** Safety blocks (severity 5) take precedence over business flags (severity 2).
- **Patience Sorting Invariant:** `tails[k]` monotonically increases with $k$. Binary search finds the smallest index $i$ such that `tails[i] >= x`.
- **Coin Change Base Case:** Initialize with `amount + 1` to prevent integer overflow when taking `Math.min(dp[i], dp[i-coin] + 1)`.
