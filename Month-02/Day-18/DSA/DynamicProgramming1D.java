import java.util.Arrays;

/**
 * 1D Dynamic Programming Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 70  - Climbing Stairs -> O(N) time, O(1) space
 *   2. LeetCode 198 - House Robber -> O(N) time, O(1) space
 *   3. LeetCode 322 - Coin Change -> O(N * amount) time, O(amount) space
 */
public class DynamicProgramming1D {

    /**
     * LC 70: Climbing Stairs
     */
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1;
        int prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    /**
     * LC 198: House Robber
     */
    public int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int rob1 = 0;
        int rob2 = 0;

        for (int n : nums) {
            int newRob = Math.max(rob2, rob1 + n);
            rob1 = rob2;
            rob2 = newRob;
        }
        return rob2;
    }

    /**
     * LC 322: Coin Change
     */
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;

        for (int a = 1; a <= amount; a++) {
            for (int c : coins) {
                if (a - c >= 0) {
                    dp[a] = Math.min(dp[a], 1 + dp[a - c]);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        DynamicProgramming1D dp = new DynamicProgramming1D();

        // 1. Climbing stairs
        System.out.println("LC 70 Climb Stairs (n=5): " + dp.climbStairs(5)); // 8

        // 2. House robber
        System.out.println("LC 198 House Robber ([2,7,9,3,1]): " + dp.rob(new int[]{2, 7, 9, 3, 1})); // 12

        // 3. Coin change
        System.out.println("LC 322 Coin Change ([1,2,5], 11): " + dp.coinChange(new int[]{1, 2, 5}, 11)); // 3
    }
}
