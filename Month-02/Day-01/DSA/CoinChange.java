import java.util.Arrays;

/**
 * LeetCode 322 - Coin Change
 * Topic: Dynamic Programming (Unbounded Knapsack)
 *
 * Problem: Given coins of different denominations and a total amount,
 * return the fewest coins needed to make up that amount, or -1 if impossible.
 *
 * Approach: Bottom-up DP
 *   dp[i] = min coins to make amount i
 *   dp[0] = 0 (base case)
 *   dp[i] = min(dp[i - coin] + 1) for each coin <= i
 *
 * Time:  O(amount * coins.length)
 * Space: O(amount)
 */
public class CoinChange {

    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
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
        CoinChange sol = new CoinChange();

        // Test 1: coins=[1,5,6,9], amount=11 -> 2 (5+6)
        System.out.println(sol.coinChange(new int[]{1, 5, 6, 9}, 11));  // 2

        // Test 2: coins=[1,2,5], amount=11 -> 3 (5+5+1)
        System.out.println(sol.coinChange(new int[]{1, 2, 5}, 11));     // 3

        // Test 3: coins=[2], amount=3 -> -1
        System.out.println(sol.coinChange(new int[]{2}, 3));            // -1

        // Test 4: amount=0 -> 0
        System.out.println(sol.coinChange(new int[]{1}, 0));            // 0
    }
}
