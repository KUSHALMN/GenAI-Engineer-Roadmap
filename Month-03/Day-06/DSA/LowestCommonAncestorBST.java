import java.util.*;

/**
 * Day 06 (Month 03) DSA: Lowest Common Ancestor (LCA)
 * - LeetCode 235: Lowest Common Ancestor of a Binary Search Tree (O(H) Time, O(1) Space)
 * - LeetCode 236: Lowest Common Ancestor of a Binary Tree (O(N) Time, O(H) Space)
 * 
 * Invariants:
 * 1. For BST (LC 235):
 *    - If both p and q are strictly less than root, LCA is in left subtree.
 *    - If both p and q are strictly greater than root, LCA is in right subtree.
 *    - Otherwise, root is the "split point" and therefore the LCA.
 * 2. For General Binary Tree (LC 236):
 *    - Post-order traversal returns non-null when a target node is found.
 *    - If both left and right calls return non-null, current node is the LCA.
 */
public class LowestCommonAncestorBST {

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
    // LC 235: LCA in BST (Iterative) - O(H) Time, O(1) Space
    // -------------------------------------------------------------
    public static TreeNode lowestCommonAncestorBST(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val && q.val < curr.val) {
                curr = curr.left;
            } else if (p.val > curr.val && q.val > curr.val) {
                curr = curr.right;
            } else {
                return curr; // Split point is the LCA
            }
        }

        return null;
    }

    // -------------------------------------------------------------
    // LC 236: LCA in General Binary Tree - O(N) Time, O(H) Space
    // -------------------------------------------------------------
    public static TreeNode lowestCommonAncestorBT(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = lowestCommonAncestorBT(root.left, p, q);
        TreeNode right = lowestCommonAncestorBT(root.right, p, q);

        if (left != null && right != null) {
            return root; // Both subtrees found a target -> root is LCA
        }

        return left != null ? left : right;
    }

    // -------------------------------------------------------------
    // Verification & Test Suite
    // -------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  Day 06 DSA: Lowest Common Ancestor Test Suite  ");
        System.out.println("=================================================\n");

        // Construct BST: [6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]
        //         6
        //       /   \
        //      2     8
        //     / \   / \
        //    0   4 7   9
        //       / \
        //      3   5
        TreeNode n0 = new TreeNode(0);
        TreeNode n3 = new TreeNode(3);
        TreeNode n5 = new TreeNode(5);
        TreeNode n4 = new TreeNode(4, n3, n5);
        TreeNode n2 = new TreeNode(2, n0, n4);

        TreeNode n7 = new TreeNode(7);
        TreeNode n9 = new TreeNode(9);
        TreeNode n8 = new TreeNode(8, n7, n9);

        TreeNode rootBST = new TreeNode(6, n2, n8);

        // Case 1: LCA of 2 and 8 in BST -> 6
        TreeNode lca1 = lowestCommonAncestorBST(rootBST, n2, n8);
        assert lca1 != null && lca1.val == 6;
        System.out.println("Case 1 (LCA of 2 and 8): " + lca1.val + " (Expected: 6) -> PASSED");

        // Case 2: LCA of 2 and 4 in BST -> 2
        TreeNode lca2 = lowestCommonAncestorBST(rootBST, n2, n4);
        assert lca2 != null && lca2.val == 2;
        System.out.println("Case 2 (LCA of 2 and 4): " + lca2.val + " (Expected: 2) -> PASSED");

        // Case 3: LCA of 3 and 5 in BST -> 4
        TreeNode lca3 = lowestCommonAncestorBST(rootBST, n3, n5);
        assert lca3 != null && lca3.val == 4;
        System.out.println("Case 3 (LCA of 3 and 5): " + lca3.val + " (Expected: 4) -> PASSED");

        // Case 4: LC 236 General Binary Tree LCA of 3 and 7 -> 6
        TreeNode lca4 = lowestCommonAncestorBT(rootBST, n3, n7);
        assert lca4 != null && lca4.val == 6;
        System.out.println("Case 4 (BT LCA of 3 and 7): " + lca4.val + " (Expected: 6) -> PASSED");

        System.out.println("\nAll Day 06 LCA tests passed successfully!");
    }
}
