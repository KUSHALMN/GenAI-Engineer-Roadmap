import java.util.*;

/**
 * Day 12: Dynamic Programming — Coin Change
 * Problem: Given coins of different denominations and a total amount of money,
 * compute the fewest number of coins needed to make up that amount.
 *
 * Algorithm:
 * - dp[a] = minimum coins needed for amount a.
 * - dp[a] = min(dp[a], dp[a - coin] + 1) for each coin <= a.
 *
 * Time Complexity: O(amount * coins.length)
 * Space Complexity: O(amount)
 */
public class CoinChangeDP {

    public int coinChange(int[] coins, int amount) {
        int max = amount + 1;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, max);
        dp[0] = 0;

        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) {
                if (coin <= a) {
                    dp[a] = Math.min(dp[a], dp[a - coin] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        CoinChangeDP solver = new CoinChangeDP();
        int[] coins = {1, 2, 5};
        int amount = 11;
        int minCoins = solver.coinChange(coins, amount);

        System.out.println("Minimum coins for amount 11: " + minCoins);
        assert minCoins == 3 : "Expected 3 coins (5 + 5 + 1 = 11)";
        System.out.println("Day 12 DSA CoinChangeDP verification passed!");
    }
}
