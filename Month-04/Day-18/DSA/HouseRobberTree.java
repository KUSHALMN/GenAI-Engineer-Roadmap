import java.util.*;

/**
 * Day 18: Tree DP — House Robber III
 * Problem: The houses form a binary tree. If two directly-linked houses are robbed, police are alerted.
 * Return the maximum amount of money you can rob.
 *
 * Algorithm:
 * - Post-order traversal (bottom-up tree DP).
 * - Each node returns an int[2]:
 *   res[0] = max loot WITHOUT robbing this node
 *   res[1] = max loot ROBBING this node
 *
 * Time Complexity: O(N) where N is number of nodes.
 * Space Complexity: O(H) recursion height.
 */
public class HouseRobberTree {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
    }

    public int rob(TreeNode root) {
        int[] result = robSub(root);
        return Math.max(result[0], result[1]);
    }

    private int[] robSub(TreeNode root) {
        if (root == null) return new int[]{0, 0};

        int[] left = robSub(root.left);
        int[] right = robSub(root.right);

        int[] res = new int[2];
        // res[0]: do NOT rob current node -> take maximum from children
        res[0] = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
        // res[1]: ROB current node -> cannot rob direct children
        res[1] = root.val + left[0] + right[0];

        return res;
    }

    public static void main(String[] args) {
        HouseRobberTree solver = new HouseRobberTree();
        // Construct:
        //      3
        //     /         //    2   3
        //     \           //      3   1
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.right = new TreeNode(3);
        root.right.right = new TreeNode(1);

        int maxMoney = solver.rob(root);
        System.out.println("Maximum robbery loot on tree: " + maxMoney);
        assert maxMoney == 7 : "Expected 7 (rob 3 + 3 + 1 = 7)";
        System.out.println("Day 18 DSA HouseRobberTree verification passed!");
    }
}
