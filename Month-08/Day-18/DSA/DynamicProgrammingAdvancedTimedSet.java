package Month_08.Day_18.DSA;

import java.util.Arrays;

/**
 * Day 18: Timed DSA Problem Set — Advanced Dynamic Programming.
 * Focus: LeetCode 300 (Longest Increasing Subsequence) & LeetCode 322 (Coin Change).
 */
public class DynamicProgrammingAdvancedTimedSet {

    // LeetCode 300: LIS using Patience Sorting / Binary Search - O(N log N) Time, O(N) Space
    public static int lengthOfLIS(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int[] tails = new int[nums.length];
        int size = 0;

        for (int x : nums) {
            int i = 0, j = size;
            while (i != j) {
                int mid = (i + j) / 2;
                if (tails[mid] < x) {
                    i = mid + 1;
                } else {
                    j = mid;
                }
            }
            tails[i] = x;
            if (i == size) size++;
        }
        return size;
    }

    // LeetCode 322: Coin Change (Unbounded Knapsack) - O(N * Amount) Time, O(Amount) Space
    public static int coinChange(int[] coins, int amount) {
        if (amount < 0) return -1;
        int max = amount + 1;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, max);
        dp[0] = 0;

        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        // LC 300 tests
        assert lengthOfLIS(new int[]{10, 9, 2, 5, 3, 7, 101, 18}) == 4 : "LIS Test 1 Failed";
        assert lengthOfLIS(new int[]{0, 1, 0, 3, 2, 3}) == 4 : "LIS Test 2 Failed";
        assert lengthOfLIS(new int[]{7, 7, 7, 7}) == 1 : "LIS Test 3 Failed";

        // LC 322 tests
        assert coinChange(new int[]{1, 2, 5}, 11) == 3 : "Coin Change Test 1 Failed";
        assert coinChange(new int[]{2}, 3) == -1 : "Coin Change Test 2 Failed";
        assert coinChange(new int[]{1}, 0) == 0 : "Coin Change Test 3 Failed";

        System.out.println("Day 18 Advanced Dynamic Programming Timed Set verification passed.");
    }
}
