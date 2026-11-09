public class DSAWeakAreaRepair {
    // 1. Binary Tree Maximum Path Sum (LC 124)
    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private static int maxSum = Integer.MIN_VALUE;

    public static int maxPathSum(TreeNode root) {
        maxSum = Integer.MIN_VALUE;
        maxGain(root);
        return maxSum;
    }

    private static int maxGain(TreeNode node) {
        if (node == null) return 0;
        int leftGain = Math.max(maxGain(node.left), 0);
        int rightGain = Math.max(maxGain(node.right), 0);
        int priceNewPath = node.val + leftGain + rightGain;
        maxSum = Math.max(maxSum, priceNewPath);
        return node.val + Math.max(leftGain, rightGain);
    }

    public static void main(String[] args) {
        System.out.println("=== DSA Weak-Area Repair & Mastery ===");
        TreeNode root = new TreeNode(-10);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);

        int ans = maxPathSum(root);
        System.out.println("LC 124 (Max Path Sum): " + ans + " (Expected 42)");
        assert ans == 42 : "LC 124 failed";
        System.out.println("DSA Weak-Area Repair passed successfully!");
    }
}
