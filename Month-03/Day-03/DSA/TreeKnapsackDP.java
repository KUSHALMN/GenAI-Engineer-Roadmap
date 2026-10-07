package DSA;

import java.util.*;

/**
 * Day 03 (Month 03) DSA: Tree Dynamic Programming & Knapsack Variations
 * - LeetCode 337: House Robber III (DP on Trees)
 * - LeetCode 416: Partition Equal Subset Sum (0-1 Knapsack DP)
 * - LeetCode 322: Coin Change (Unbounded Knapsack DP)
 */
public class TreeKnapsackDP {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;
        public TreeNode(int val) {
            this.val = val;
        }
    }

    // -------------------------------------------------------------
    // LC 337: House Robber III (Tree DP)
    // -------------------------------------------------------------
    public static int rob(TreeNode root) {
        int[] result = robDfs(root);
        return Math.max(result[0], result[1]);
    }

    // Returns int[]{robThisNode, notRobThisNode}
    private static int[] robDfs(TreeNode node) {
        if (node == null) return new int[]{0, 0};

        int[] left = robDfs(node.left);
        int[] right = robDfs(node.right);

        // If we rob this node, cannot rob children
        int robThis = node.val + left[1] + right[1];

        // If we do not rob this node, can either rob or not rob children
        int notRobThis = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);

        return new int[]{robThis, notRobThis};
    }

    // -------------------------------------------------------------
    // LC 416: Partition Equal Subset Sum (0-1 Knapsack)
    // -------------------------------------------------------------
    public static boolean canPartition(int[] nums) {
        int totalSum = 0;
        for (int num : nums) totalSum += num;
        if (totalSum % 2 != 0) return false;

        int target = totalSum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : nums) {
            // Traverse backwards to prevent using the same element multiple times
            for (int j = target; j >= num; j--) {
                dp[j] = dp[j] || dp[j - num];
            }
        }
        return dp[target];
    }

    // -------------------------------------------------------------
    // LC 322: Coin Change (Unbounded Knapsack)
    // -------------------------------------------------------------
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;

        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (i >= coin) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Month 03 Day 03: Tree DP & Knapsack DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 337 House Robber III
        //       3
        //      / \
        //     2   3
        //      \   \
        //       3   1
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.right = new TreeNode(3);
        root.right.right = new TreeNode(1);

        int maxLoot = rob(root);
        System.out.println("LC 337 (House Robber III Max Loot): " + maxLoot);
        assert maxLoot == 7 : "LC 337 Failed";

        // Test 2: LC 416 Partition Equal Subset Sum
        int[] nums1 = {1, 5, 11, 5};
        boolean canPart = canPartition(nums1);
        System.out.println("LC 416 (Can Partition [1,5,11,5]): " + canPart);
        assert canPart : "LC 416 Failed";

        // Test 3: LC 322 Coin Change
        int[] coins = {1, 2, 5};
        int amount = 11;
        int minCoins = coinChange(coins, amount);
        System.out.println("LC 322 (Coin Change for 11): " + minCoins);
        assert minCoins == 3 : "LC 322 Failed"; // 5 + 5 + 1

        System.out.println("\nAll Java Tree DP & Knapsack tests executed successfully! [OK]");
    }
}
