package Month_09.Day_18.DSA;

/**
 * Day 18: Timed DSA Problem Set — Advanced Interval Dynamic Programming.
 * Focus: LeetCode 312 (Burst Balloons) - O(N^3) Time, O(N^2) Space.
 */
public class BurstBalloonsTimedSet {

    public static int maxCoins(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int n = nums.length;
        // Pad with virtual balloons of value 1 at boundaries
        int[] arr = new int[n + 2];
        arr[0] = 1;
        arr[n + 1] = 1;
        for (int i = 0; i < n; i++) {
            arr[i + 1] = nums[i];
        }

        int[][] dp = new int[n + 2][n + 2];

        // Length of interval from 1 to n
        for (int len = 1; len <= n; len++) {
            for (int left = 1; left <= n - len + 1; left++) {
                int right = left + len - 1;

                // Pick balloon k to be the LAST balloon burst in interval [left, right]
                for (int k = left; k <= right; k++) {
                    int coins = dp[left][k - 1] + dp[k + 1][right] + (arr[left - 1] * arr[k] * arr[right + 1]);
                    dp[left][right] = Math.max(dp[left][right], coins);
                }
            }
        }
        return dp[1][n];
    }

    public static void main(String[] args) {
        assert maxCoins(new int[]{3, 1, 5, 8}) == 167 : "Test 1 Failed";
        assert maxCoins(new int[]{1, 5}) == 10 : "Test 2 Failed";
        assert maxCoins(new int[]{7}) == 7 : "Test 3 Failed";

        System.out.println("Day 18 Burst Balloons Timed Set verification passed.");
    }
}
