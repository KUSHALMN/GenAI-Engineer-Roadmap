package Month_09.Day_01.DSA;

/**
 * Day 01: Timed DSA Problem Set — 0/1 Knapsack & Partition Equal Subset Sum.
 * Focus: LeetCode 416 (Partition Equal Subset Sum) - O(N * Target) Time, O(Target) Space.
 */
public class KnapsackZeroOneTimedSet {

    // LeetCode 416: Partition Equal Subset Sum - 1D DP Space Optimization
    public static boolean canPartition(int[] nums) {
        if (nums == null || nums.length < 2) return false;
        int totalSum = 0;
        for (int num : nums) totalSum += num;
        if (totalSum % 2 != 0) return false;

        int target = totalSum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : nums) {
            // Iterate backwards to prevent using the same element multiple times
            for (int w = target; w >= num; w--) {
                dp[w] = dp[w] || dp[w - num];
            }
        }
        return dp[target];
    }

    // Classic 0/1 Knapsack: returns maximum value within capacity
    public static int knapsack(int[] values, int[] weights, int capacity) {
        int[] dp = new int[capacity + 1];
        for (int i = 0; i < values.length; i++) {
            for (int w = capacity; w >= weights[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        return dp[capacity];
    }

    public static void main(String[] args) {
        // LC 416 tests
        assert canPartition(new int[]{1, 5, 11, 5}) : "LC 416 Test 1 Failed";
        assert !canPartition(new int[]{1, 2, 3, 5}) : "LC 416 Test 2 Failed";
        assert canPartition(new int[]{2, 2, 3, 5}) : "LC 416 Test 3 Failed";

        // Knapsack tests
        int[] vals = {60, 100, 120};
        int[] weights = {10, 20, 30};
        assert knapsack(vals, weights, 50) == 220 : "Knapsack Test 1 Failed";

        System.out.println("Day 01 0/1 Knapsack Timed Set verification passed.");
    }
}
