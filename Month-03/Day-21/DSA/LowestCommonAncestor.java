package DSA;

/**
 * Lowest Common Ancestor (LCA) in Binary Tree & BST
 * 1. LeetCode 236 - LCA of Binary Tree
 *    Post-order DFS:
 *    - Base cases: node == null, or node == p, or node == q -> return node
 *    - Recursively search left and right subtrees
 *    - If both left and right return non-null, current node is the LCA
 *    - Otherwise return whichever child is non-null
 *    Complexity: Time O(N), Space O(H) where H is tree height.
 * 
 * 2. LeetCode 235 - LCA of Binary Search Tree
 *    Uses BST ordering property:
 *    - If both p and q < root.val -> go left
 *    - If both p and q > root.val -> go right
 *    - Otherwise, split point is the LCA
 *    Complexity: Time O(H), Space O(1) iterative.
 */
public class LowestCommonAncestor {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    /**
     * LC 236: Lowest Common Ancestor in General Binary Tree
     */
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);

        if (left != null && right != null) {
            return root; // p and q are in separate subtrees -> root is LCA
        }

        return left != null ? left : right;
    }

    /**
     * LC 235: Lowest Common Ancestor in Binary Search Tree
     */
    public static TreeNode lowestCommonAncestorBST(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode curr = root;
        while (curr != null) {
            if (p.val < curr.val && q.val < curr.val) {
                curr = curr.left;
            } else if (p.val > curr.val && q.val > curr.val) {
                curr = curr.right;
            } else {
                return curr; // Split point
            }
        }
        return null;
    }

    public static void main(String[] args) {
        // Construct Binary Tree:
        //        3
        //       / \
        //      5   1
        //     / \
        //    6   2
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(5);
        root.right = new TreeNode(1);
        root.left.left = new TreeNode(6);
        root.left.right = new TreeNode(2);

        TreeNode p = root.left; // Node 5
        TreeNode q = root.right; // Node 1
        TreeNode lca = lowestCommonAncestor(root, p, q);
        System.out.println("LCA of 5 and 1: " + lca.val + " (Expected: 3)");

        TreeNode p2 = root.left.left; // Node 6
        TreeNode q2 = root.left.right; // Node 2
        TreeNode lca2 = lowestCommonAncestor(root, p2, q2);
        System.out.println("LCA of 6 and 2: " + lca2.val + " (Expected: 5)");

        System.out.println("LowestCommonAncestor tests passed!");
    }
}
