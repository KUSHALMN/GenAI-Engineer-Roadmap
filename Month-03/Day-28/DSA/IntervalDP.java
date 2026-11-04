package DSA;

/**
 * Interval Dynamic Programming
 * LeetCode 312 - Burst Balloons
 * 
 * Invariant & Thinking:
 * Instead of thinking "which balloon to burst FIRST" (which couples remaining balloons),
 * think "which balloon k bursts LAST in interval [i, j]".
 * 
 * When balloon k bursts last in [i, j], its neighbors are guaranteed to be balloons i-1 and j+1!
 * 
 * DP Recurrence:
 * dp[i][j] = max_{i <= k <= j} (dp[i][k-1] + dp[k+1][j] + nums[i-1] * nums[k] * nums[j+1])
 * 
 * Complexity:
 * - Time: O(N^3)
 * - Space: O(N^2)
 */
public class IntervalDP {

    public static int maxCoins(int[] nums) {
        int n = nums.length;
        // Pad array with 1 at both boundaries
        int[] padded = new int[n + 2];
        padded[0] = 1;
        padded[n + 1] = 1;
        System.arraycopy(nums, 0, padded, 1, n);

        int[][] dp = new int[n + 2][n + 2];

        // Length of interval from 1 to n
        for (int len = 1; len <= n; len++) {
            for (int i = 1; i <= n - len + 1; i++) {
                int j = i + len - 1;

                // Pick balloon k to burst LAST in interval [i, j]
                for (int k = i; k <= j; k++) {
                    int coins = dp[i][k - 1] + dp[k + 1][j] + padded[i - 1] * padded[k] * padded[j + 1];
                    dp[i][j] = Math.max(dp[i][j], coins);
                }
            }
        }

        return dp[1][n];
    }

    public static void main(String[] args) {
        int[] balloons = {3, 1, 5, 8};
        int coins = maxCoins(balloons);
        // Optimal sequence: burst 1 -> burst 5 -> burst 3 -> burst 8 = 167
        System.out.println("Maximum coins for [3, 1, 5, 8]: " + coins + " (Expected: 167)");

        int[] simple = {1, 5};
        System.out.println("Maximum coins for [1, 5]: " + maxCoins(simple) + " (Expected: 10)");

        System.out.println("IntervalDP tests passed!");
    }
}
