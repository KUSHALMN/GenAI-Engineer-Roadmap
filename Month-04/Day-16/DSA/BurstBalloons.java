import java.util.*;

/**
 * Day 16: Interval DP — Burst Balloons
 * Problem: Given n balloons, indexed from 0 to n - 1. Each balloon is painted with a number on it.
 * Burst balloon i to gain nums[i - 1] * nums[i] * nums[i + 1] coins. Return the maximum coins you can collect.
 *
 * Algorithm:
 * - Pad nums with 1 on left and right.
 * - dp[i][j] = maximum coins collected by bursting all balloons between i and j (excluding i and j).
 * - Consider the LAST balloon k burst in (i, j):
 *   dp[i][j] = max(dp[i][j], dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j])
 *
 * Time Complexity: O(n^3)
 * Space Complexity: O(n^2)
 */
public class BurstBalloons {

    public int maxCoins(int[] nums) {
        int n = nums.length;
        int[] padded = new int[n + 2];
        padded[0] = 1;
        padded[n + 1] = 1;
        for (int i = 0; i < n; i++) padded[i + 1] = nums[i];

        int[][] dp = new int[n + 2][n + 2];

        // Length of interval from 1 to n
        for (int len = 1; len <= n; len++) {
            for (int left = 1; left <= n - len + 1; left++) {
                int right = left + len - 1;
                for (int k = left; k <= right; k++) {
                    int coins = padded[left - 1] * padded[k] * padded[right + 1];
                    coins += dp[left][k - 1] + dp[k + 1][right];
                    dp[left][right] = Math.max(dp[left][right], coins);
                }
            }
        }
        return dp[1][n];
    }

    public static void main(String[] args) {
        BurstBalloons solver = new BurstBalloons();
        int[] nums = {3, 1, 5, 8};
        int coins = solver.maxCoins(nums);

        System.out.println("Maximum coins for [3, 1, 5, 8]: " + coins);
        assert coins == 167 : "Expected 167 coins";
        System.out.println("Day 16 DSA BurstBalloons verification passed!");
    }
}
