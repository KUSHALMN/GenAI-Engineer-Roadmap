public class validate_bst {
    // LeetCode #98 - Validate Binary Search Tree
    // Approach: Recursive DFS with Min/Max range constraints
    // Time Complexity: O(n) visiting each node once
    // Space Complexity: O(h) recursion stack space

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    public boolean isValidBST(TreeNode root) {
        return validate(root, null, null);
    }

    private boolean validate(TreeNode node, Integer min, Integer max) {
        if (node == null) return true;

        if ((min != null && node.val <= min) || (max != null && node.val >= max)) {
            return false;
        }

        return validate(node.left, min, node.val) && validate(node.right, node.val, max);
    }

    public static void main(String[] args) {
        validate_bst solution = new validate_bst();

        // Valid BST: [2, 1, 3]
        TreeNode validRoot = new TreeNode(2, new TreeNode(1), new TreeNode(3));
        System.out.println("Is [2, 1, 3] valid BST? " + solution.isValidBST(validRoot)); // true

        // Invalid BST: [5, 1, 4, null, null, 3, 6]
        TreeNode invalidRoot = new TreeNode(5);
        invalidRoot.left = new TreeNode(1);
        invalidRoot.right = new TreeNode(4, new TreeNode(3), new TreeNode(6));
        System.out.println("Is [5, 1, 4, 3, 6] valid BST? " + solution.isValidBST(invalidRoot)); // false
    }
}
