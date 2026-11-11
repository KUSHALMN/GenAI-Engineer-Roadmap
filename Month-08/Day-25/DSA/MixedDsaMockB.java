package Month_08.Day_25.DSA;

/**
 * Day 25: Timed DSA Problem Set — Mixed Hard Mock Set B.
 * Focus: LeetCode 124 (Binary Tree Maximum Path Sum) & LeetCode 312 (Burst Balloons).
 */
public class MixedDsaMockB {

    // LeetCode 124: TreeNode
    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private static int maxPathSumVal;

    // LeetCode 124: Binary Tree Maximum Path Sum - O(N) Time, O(H) Space
    public static int maxPathSum(TreeNode root) {
        maxPathSumVal = Integer.MIN_VALUE;
        maxGain(root);
        return maxPathSumVal;
    }

    private static int maxGain(TreeNode node) {
        if (node == null) return 0;
        int leftGain = Math.max(maxGain(node.left), 0);
        int rightGain = Math.max(maxGain(node.right), 0);

        int currentPathSum = node.val + leftGain + rightGain;
        maxPathSumVal = Math.max(maxPathSumVal, currentPathSum);

        return node.val + Math.max(leftGain, rightGain);
    }

    // LeetCode 312: Burst Balloons - O(N^3) Time, O(N^2) Space (Interval DP)
    public static int maxCoins(int[] nums) {
        int n = nums.length;
        int[] arr = new int[n + 2];
        arr[0] = 1;
        arr[n + 1] = 1;
        for (int i = 0; i < n; i++) {
            arr[i + 1] = nums[i];
        }

        int[][] dp = new int[n + 2][n + 2];

        // length from 1 to n
        for (int len = 1; len <= n; len++) {
            for (int left = 1; left <= n - len + 1; left++) {
                int right = left + len - 1;
                for (int k = left; k <= right; k++) {
                    int coins = dp[left][k - 1] + dp[k + 1][right] + arr[left - 1] * arr[k] * arr[right + 1];
                    dp[left][right] = Math.max(dp[left][right], coins);
                }
            }
        }
        return dp[1][n];
    }

    public static void main(String[] args) {
        // LC 124 tests
        TreeNode root = new TreeNode(-10);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        assert maxPathSum(root) == 42 : "MaxPathSum Test 1 Failed";

        // LC 312 tests
        assert maxCoins(new int[]{3, 1, 5, 8}) == 167 : "Burst Balloons Test 1 Failed";
        assert maxCoins(new int[]{1, 5}) == 10 : "Burst Balloons Test 2 Failed";

        System.out.println("Day 25 Mixed Hard Mock Set B verification passed.");
    }
}
