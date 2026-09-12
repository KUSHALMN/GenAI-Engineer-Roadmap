/**
 * LeetCode 70 - Climbing Stairs
 * Topic: Dynamic Programming (Fibonacci variant)
 *
 * Problem: You can climb 1 or 2 steps at a time.
 * How many distinct ways to reach the top of n stairs?
 *
 * Recurrence:
 *   dp[i] = dp[i-1] + dp[i-2]   (same as Fibonacci)
 *
 * Space Optimization: Only need prev2 and prev1.
 *
 * Time:  O(n)
 * Space: O(1)
 */
public class ClimbingStairs {

    public int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1, prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    // Extension: climb 1, 2, or 3 steps (tribonacci variant)
    public int climbStairsK(int n, int k) {
        if (n == 0) return 1;
        int[] dp = new int[n + 1];
        dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= k && j <= i; j++) {
                dp[i] += dp[i - j];
            }
        }
        return dp[n];
    }

    public static void main(String[] args) {
        ClimbingStairs sol = new ClimbingStairs();

        System.out.println(sol.climbStairs(1));   // 1
        System.out.println(sol.climbStairs(2));   // 2
        System.out.println(sol.climbStairs(3));   // 3
        System.out.println(sol.climbStairs(5));   // 8
        System.out.println(sol.climbStairs(10));  // 89

        // k=3 steps variant
        System.out.println(sol.climbStairsK(3, 3)); // 4
        System.out.println(sol.climbStairsK(5, 3)); // 13
    }
}
