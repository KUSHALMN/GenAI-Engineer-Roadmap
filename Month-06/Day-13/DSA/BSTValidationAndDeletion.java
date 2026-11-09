/**
 * Binary Search Tree (BST) Patterns Revision
 * Solves core FAANG interview problems:
 * 1. Validate Binary Search Tree (LC 98) with strict bounds
 * 2. Kth Smallest Element in a BST (LC 230) using in-order traversal
 * 3. Delete Node in a BST (LC 450) preserving BST invariant
 */

public class BSTValidationAndDeletion {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
    }

    // 1. LC 98: Validate BST
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

    // 2. LC 230: Kth Smallest Element in BST
    private static int count = 0;
    private static int kthResult = -1;

    public static int kthSmallest(TreeNode root, int k) {
        count = 0;
        kthResult = -1;
        inorderKth(root, k);
        return kthResult;
    }

    private static void inorderKth(TreeNode node, int k) {
        if (node == null || kthResult != -1) return;
        inorderKth(node.left, k);
        count++;
        if (count == k) {
            kthResult = node.val;
            return;
        }
        inorderKth(node.right, k);
    }

    // 3. LC 450: Delete Node in a BST
    public static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Node found: 3 cases
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;

            // Node has two children: find inorder successor (smallest in right subtree)
            TreeNode successor = findMin(root.right);
            root.val = successor.val;
            root.right = deleteNode(root.right, successor.val);
        }
        return root;
    }

    private static TreeNode findMin(TreeNode node) {
        while (node.left != null) node = node.left;
        return node;
    }

    public static void main(String[] args) {
        System.out.println("=== BST Validation & Deletion Verification ===");

        // Valid BST:
        //       5
        //      /         //     3   6
        //    /         //   2   4
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(6);
        root.left.left = new TreeNode(2);
        root.left.right = new TreeNode(4);

        assert isValidBST(root) : "BST validation failed";
        System.out.println("LC 98: Tree is a valid BST -> true");

        int k3 = kthSmallest(root, 3);
        System.out.println("LC 230: 3rd Smallest Element -> " + k3 + " (Expected 4)");
        assert k3 == 4 : "LC 230 failed";

        TreeNode modified = deleteNode(root, 3);
        assert isValidBST(modified) : "BST property corrupted after delete";
        System.out.println("LC 450: Deleted node 3 successfully while preserving BST property!");
    }
}
