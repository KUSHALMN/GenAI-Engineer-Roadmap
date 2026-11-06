import java.util.*;

/**
 * Day 11: Dynamic Programming — 0/1 Knapsack & Partition Equal Subset Sum
 * Problem: Given array nums, determine if it can be partitioned into two subsets with equal sum.
 *
 * Algorithm:
 * - Target = sum(nums) / 2. If sum is odd, impossible.
 * - dp[w] = boolean whether sum w is achievable.
 * - Iterate backwards from target down to num to reuse single 1D array.
 *
 * Time Complexity: O(n * target)
 * Space Complexity: O(target)
 */
public class Knapsack01 {

    public boolean canPartition(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        if (total % 2 != 0) return false;

        int target = total / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : nums) {
            for (int w = target; w >= num; w--) {
                dp[w] = dp[w] || dp[w - num];
            }
        }
        return dp[target];
    }

    public static void main(String[] args) {
        Knapsack01 solver = new Knapsack01();
        int[] nums1 = {1, 5, 11, 5};
        int[] nums2 = {1, 2, 3, 5};

        assert solver.canPartition(nums1) : "Expected true for [1, 5, 11, 5] -> subsets {11} and {1,5,5}";
        assert !solver.canPartition(nums2) : "Expected false for [1, 2, 3, 5]";
        System.out.println("Day 11 DSA Knapsack01 verification passed!");
    }
}
