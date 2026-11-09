public class DynamicProgramming1DRevision {
    // 1. LC 70: Climbing Stairs
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }

    // 2. LC 198: House Robber
    public static int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int prev1 = 0, prev2 = 0;
        for (int num : nums) {
            int tmp = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = tmp;
        }
        return prev1;
    }

    // 3. LC 322: Coin Change
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        java.util.Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int c : coins) {
                if (i - c >= 0) {
                    dp[i] = Math.min(dp[i], dp[i - c] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        System.out.println("=== 1D Dynamic Programming Verification ===");
        assert climbStairs(5) == 8 : "LC 70 failed";
        System.out.println("LC 70 (Climbing Stairs n=5): 8 ways");

        int[] houses = {2, 7, 9, 3, 1};
        assert rob(houses) == 12 : "LC 198 failed";
        System.out.println("LC 198 (House Robber): 12 max loot");

        int[] coins = {1, 2, 5};
        assert coinChange(coins, 11) == 3 : "LC 322 failed";
        System.out.println("LC 322 (Coin Change 11): 3 coins");
        System.out.println("1D DP tests passed!");
    }
}
