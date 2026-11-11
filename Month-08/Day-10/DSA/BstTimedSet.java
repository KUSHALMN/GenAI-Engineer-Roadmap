package Month08.Day10;

/**
 * Timed Set: Binary Search Trees (BST)
 * LC 98: Validate Binary Search Tree - O(N) time with range boundary invariants.
 */
public class BstTimedSet {

    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    public static boolean isValidBST(TreeNode root) {
        return validate(root, null, null);
    }

    private static boolean validate(TreeNode node, Integer min, Integer max) {
        if (node == null) return true;
        if ((min != null && node.val <= min) || (max != null && node.val >= max)) {
            return false;
        }
        return validate(node.left, min, node.val) && validate(node.right, node.val, max);
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(2);
        root.left = new TreeNode(1);
        root.right = new TreeNode(3);
        assert isValidBST(root);

        TreeNode bad = new TreeNode(5);
        bad.left = new TreeNode(1);
        bad.right = new TreeNode(4); // Invalid: 4 < 5
        assert !isValidBST(bad);

        System.out.println("Day 10 BST Timed Set verification passed.");
    }
}
