/**
 * Binary Search Tree Operations in Java
 *
 * Problems Covered:
 *   1. LeetCode 700 - Search in a BST -> O(H) time, O(1) space
 *   2. LeetCode 701 - Insert into a BST -> O(H) time, O(H) space
 *   3. LeetCode 450 - Delete Node in a BST -> O(H) time, O(H) space
 *   4. LeetCode 98  - Validate Binary Search Tree -> O(N) time, O(H) space
 *   5. LeetCode 235 - Lowest Common Ancestor of a BST -> O(H) time, O(1) space
 */
public class BinarySearchTree {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode() {}
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    /**
     * LC 700: Search in a BST
     */
    public TreeNode searchBST(TreeNode root, int val) {
        TreeNode curr = root;
        while (curr != null) {
            if (curr.val == val) return curr;
            else if (val < curr.val) curr = curr.left;
            else curr = curr.right;
        }
        return null;
    }

    /**
     * LC 701: Insert into a BST
     */
    public TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);
        if (val < root.val) root.left = insertIntoBST(root.left, val);
        else root.right = insertIntoBST(root.right, val);
        return root;
    }

    /**
     * LC 450: Delete Node in a BST
     */
    public TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Node found
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;

            // Find inorder successor (min in right subtree)
            TreeNode successor = root.right;
            while (successor.left != null) {
                successor = successor.left;
            }
            root.val = successor.val;
            root.right = deleteNode(root.right, successor.val);
        }
        return root;
    }

    /**
     * LC 98: Validate Binary Search Tree
     */
    public boolean isValidBST(TreeNode root) {
        return validate(root, null, null);
    }

    private boolean validate(TreeNode node, Integer low, Integer high) {
        if (node == null) return true;
        if ((low != null && node.val <= low) || (high != null && node.val >= high)) {
            return false;
        }
        return validate(node.left, low, node.val) && validate(node.right, node.val, high);
    }

    /**
     * LC 235: Lowest Common Ancestor of a BST
     */
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode curr = root;
        while (curr != null) {
            if (p.val > curr.val && q.val > curr.val) {
                curr = curr.right;
            } else if (p.val < curr.val && q.val < curr.val) {
                curr = curr.left;
            } else {
                return curr;
            }
        }
        return null;
    }

    public static void main(String[] args) {
        BinarySearchTree bst = new BinarySearchTree();

        // 1. Insert & Build BST
        TreeNode root = new TreeNode(6);
        bst.insertIntoBST(root, 2);
        bst.insertIntoBST(root, 8);
        bst.insertIntoBST(root, 0);
        bst.insertIntoBST(root, 4);

        // 2. Validate BST
        System.out.println("Is Valid BST: " + bst.isValidBST(root)); // true

        // 3. Search
        TreeNode found = bst.searchBST(root, 4);
        System.out.println("Search 4 Found: " + (found != null ? found.val : "null")); // 4

        // 4. LCA
        TreeNode p = bst.searchBST(root, 0);
        TreeNode q = bst.searchBST(root, 4);
        TreeNode lca = bst.lowestCommonAncestor(root, p, q);
        System.out.println("LCA of 0 and 4: " + lca.val); // 2

        // 5. Delete Node 2
        root = bst.deleteNode(root, 2);
        System.out.println("Deleted 2, Search 2: " + (bst.searchBST(root, 2) != null)); // false
        System.out.println("Is Still Valid BST: " + bst.isValidBST(root)); // true
    }
}
