# Day 33 (Month 02 - Day 03): Coding Interview Questions
## Focus: Dynamic Programming — House Robber (LC 198 & 213)

---

### Q1: Derive the House Robber recurrence from scratch.

**Answer:**
- **State**: `dp[i]` = max money robbing from houses `0..i`
- **Choice at house i**:
  - **Rob it**: get `nums[i]` + best from `0..i-2` → `dp[i-2] + nums[i]`
  - **Skip it**: best from `0..i-1` → `dp[i-1]`
- **Recurrence**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
- **Base cases**: `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`

**Space optimization**: Since `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, replace the array with two variables `prev1`, `prev2`:
```java
int curr = Math.max(prev1, prev2 + num);
prev2 = prev1;
prev1 = curr;
```
Reduces space from O(n) → O(1).

---

### Q2: How does House Robber II (LC 213, circular array) extend the solution?

**Answer:**
- **Constraint**: First and last house are adjacent (circular), so you can't rob both.
- **Key insight**: Either house `0` is robbed (exclude last) OR house `n-1` is robbed (exclude first). Never both.
- **Solution**: Run linear House Robber twice:
  1. `robRange(nums, 0, n-2)` — exclude last house
  2. `robRange(nums, 1, n-1)` — exclude first house
  3. Return `max` of both results
- **Why this works**: By excluding one endpoint, we break the circular constraint and reduce to the linear problem.

**Trace** — `[2, 3, 2]`:
- Range `[0,1]` → rob `[2,3]` → max=3
- Range `[1,2]` → rob `[3,2]` → max=3
- Answer: `max(3,3)` = **3** ✅

---

### Q3: What DP pattern family does House Robber belong to, and what are similar problems?

**Answer:**
- **Pattern**: 1D DP with "skip adjacent" constraint — a subset of **decision DP**.
- **Similar problems**:
  | Problem | Twist |
  |---------|-------|
  | LC 213 House Robber II | Circular array |
  | LC 337 House Robber III | Binary tree (DFS + DP) |
  | LC 740 Delete and Earn | Map values to house robber |
  | LC 1388 Pizza With 3n Slices | Circular + pick n/3 items |
- **LC 740 reduction**: `earn[i] = i * count(i)` → robbing `earn[i]` deletes `i-1` and `i+1` → identical to House Robber on the `earn` array.

---

### Q4: What is the time/space complexity and can it be solved with memoization (top-down)?

**Answer:**
- **Bottom-up (iterative)**: Time O(n), Space O(1) — optimal.
- **Top-down (memoization)**:
```java
Map<Integer, Integer> memo = new HashMap<>();

int dp(int[] nums, int i) {
    if (i < 0) return 0;
    if (memo.containsKey(i)) return memo.get(i);
    int result = Math.max(dp(nums, i-1), dp(nums, i-2) + nums[i]);
    memo.put(i, result);
    return result;
}
```
  - Time O(n), Space O(n) for memo + O(n) call stack.
- **Bottom-up is preferred** in interviews: no recursion overhead, O(1) space after optimization, no risk of stack overflow on large inputs.
