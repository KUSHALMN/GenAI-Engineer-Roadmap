import java.util.*;

/**
 * Day 05 (Month 03) DSA: Validate & Recover Binary Search Tree (BST)
 * - LeetCode 98: Validate Binary Search Tree (Range Bounds + Inorder Traversal)
 * - LeetCode 99: Recover Binary Search Tree (Two Swapped Nodes Recovery)
 * 
 * Invariants:
 * 1. For every node N in a valid BST:
 *    All keys in left subtree < N.val < all keys in right subtree.
 * 2. Inorder traversal of a valid BST is strictly monotonically increasing.
 */
public class ValidateBST {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // -------------------------------------------------------------
    // LC 98: Validate BST via Range Bounds - O(N) Time, O(H) Space
    // -------------------------------------------------------------
    public static boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        if (node.val <= min || node.val >= max) return false;

        return validate(node.left, min, node.val) && validate(node.right, node.val, max);
    }

    // -------------------------------------------------------------
    // LC 98 Alternative: Iterative Inorder Traversal - O(N) Time, O(H) Space
    // -------------------------------------------------------------
    public static boolean isValidBSTInorder(TreeNode root) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;
        Integer prev = null;

        while (curr != null || !stack.isEmpty()) {
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            if (prev != null && curr.val <= prev) {
                return false;
            }
            prev = curr.val;

            curr = curr.right;
        }

        return true;
    }

    // -------------------------------------------------------------
    // LC 99: Recover BST - O(N) Time, O(H) Space
    // Exactly two nodes of a BST were swapped by mistake. Recover without changing structure.
    // -------------------------------------------------------------
    public static class BSTRecoverer {
        private TreeNode first = null;
        private TreeNode second = null;
        private TreeNode prev = null;

        public void recoverTree(TreeNode root) {
            first = null;
            second = null;
            prev = null;

            inorder(root);

            if (first != null && second != null) {
                int temp = first.val;
                first.val = second.val;
                second.val = temp;
            }
        }

        private void inorder(TreeNode curr) {
            if (curr == null) return;

            inorder(curr.left);

            if (prev != null && prev.val > curr.val) {
                if (first == null) {
                    first = prev; // First violation
                }
                second = curr; // Second violation or adjacent node
            }
            prev = curr;

            inorder(curr.right);
        }
    }

    // -------------------------------------------------------------
    // Verification & Test Suite
    // -------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  Day 05 DSA: Validate & Recover BST Test Suite  ");
        System.out.println("=================================================\n");

        // Case 1: Valid BST [2, 1, 3]
        TreeNode validTree = new TreeNode(2, new TreeNode(1), new TreeNode(3));
        assert isValidBST(validTree);
        assert isValidBSTInorder(validTree);
        System.out.println("Case 1 (Valid [2, 1, 3]): PASSED");

        // Case 2: Invalid BST [5, 1, 4, null, null, 3, 6]
        TreeNode invalidTree = new TreeNode(5, new TreeNode(1), new TreeNode(4, new TreeNode(3), new TreeNode(6)));
        assert !isValidBST(invalidTree);
        assert !isValidBSTInorder(invalidTree);
        System.out.println("Case 2 (Invalid [5, 1, 4...]): PASSED");

        // Case 3: LC 99 Recover Tree: [1, 3, null, null, 2] -> 1 and 3 swapped
        //      1
        //     /
        //    3
        //     \
        //      2
        TreeNode swappedTree = new TreeNode(1);
        swappedTree.left = new TreeNode(3, null, new TreeNode(2));

        assert !isValidBST(swappedTree);
        BSTRecoverer recoverer = new BSTRecoverer();
        recoverer.recoverTree(swappedTree);
        assert isValidBST(swappedTree);
        System.out.println("Case 3 (Recover BST LC 99): PASSED");

        System.out.println("\nAll Day 05 Validate & Recover BST tests passed successfully!");
    }
}
