package Month08.Day09;

/**
 * Timed Set: Binary Trees
 * LC 104: Maximum Depth of Binary Tree - O(N) time with postorder recursion.
 */
public class BinaryTreesTimedSet {

    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    public static int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);

        assert maxDepth(root) == 3;
        System.out.println("Day 09 Binary Trees Timed Set verification passed.");
    }
}
