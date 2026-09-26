"""
1D Dynamic Programming Patterns (Python).
Problems Implemented:
1. Climbing Stairs (LC 70) - O(N) time, O(1) space
2. House Robber (LC 198) - O(N) time, O(1) space
3. Coin Change (LC 322) - O(Amount * Coins) time, O(Amount) space
4. Longest Increasing Subsequence (LC 300) - O(N log N) binary search / O(N^2) DP
"""

import bisect
from typing import List


class DynamicProgramming1D:

    @staticmethod
    def climb_stairs(n: int) -> int:
        """LC 70: Climbing Stairs (Fibonacci recurrence)."""
        if n <= 2:
            return n
        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
        return prev1

    @staticmethod
    def rob(nums: List[int]) -> int:
        """LC 198: House Robber (Non-adjacent maximum sum)."""
        if not nums:
            return 0
        rob1, rob2 = 0, 0
        for n in nums:
            new_rob = max(rob2, rob1 + n)
            rob1 = rob2
            rob2 = new_rob
        return rob2

    @staticmethod
    def coin_change(coins: List[int], amount: int) -> int:
        """LC 322: Coin Change (Fewest coins to make amount)."""
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0

        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])

        return dp[amount] if dp[amount] != float("inf") else -1

    @staticmethod
    def length_of_lis(nums: List[int]) -> int:
        """LC 300: Longest Increasing Subsequence via Patience Sorting (O(N log N))."""
        tails = []
        for x in nums:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x
        return len(tails)


if __name__ == "__main__":
    dp = DynamicProgramming1D()

    # LC 70
    assert dp.climb_stairs(2) == 2
    assert dp.climb_stairs(3) == 3
    assert dp.climb_stairs(5) == 8

    # LC 198
    assert dp.rob([1, 2, 3, 1]) == 4
    assert dp.rob([2, 7, 9, 3, 1]) == 12

    # LC 322
    assert dp.coin_change([1, 2, 5], 11) == 3
    assert dp.coin_change([2], 3) == -1
    assert dp.coin_change([1], 0) == 0

    # LC 300
    assert dp.length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    print("All 1D Dynamic Programming Python tests passed successfully!")
