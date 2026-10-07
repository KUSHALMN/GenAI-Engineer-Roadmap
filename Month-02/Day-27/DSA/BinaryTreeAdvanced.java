package DSA;

import java.util.*;

/**
 * Day 27 DSA: Advanced Binary Tree Algorithms
 * - LeetCode 543: Diameter of Binary Tree
 * - LeetCode 124: Binary Tree Maximum Path Sum (Hard)
 * - LeetCode 297: Serialize and Deserialize Binary Tree (Hard)
 */
public class BinaryTreeAdvanced {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;
        public TreeNode(int val) {
            this.val = val;
        }
    }

    // ---------------------------------------------------------
    // LC 543: Diameter of Binary Tree
    // ---------------------------------------------------------
    private static int maxDiameter = 0;

    public static int diameterOfBinaryTree(TreeNode root) {
        maxDiameter = 0;
        depthDFS(root);
        return maxDiameter;
    }

    private static int depthDFS(TreeNode node) {
        if (node == null) return 0;
        int leftDepth = depthDFS(node.left);
        int rightDepth = depthDFS(node.right);
        maxDiameter = Math.max(maxDiameter, leftDepth + rightDepth);
        return 1 + Math.max(leftDepth, rightDepth);
    }

    // ---------------------------------------------------------
    // LC 124: Binary Tree Maximum Path Sum
    // ---------------------------------------------------------
    private static int maxPathSumVal = Integer.MIN_VALUE;

    public static int maxPathSum(TreeNode root) {
        maxPathSumVal = Integer.MIN_VALUE;
        pathDFS(root);
        return maxPathSumVal;
    }

    private static int pathDFS(TreeNode node) {
        if (node == null) return 0;
        // Ignore negative path sums by taking Math.max(0, ...)
        int leftGain = Math.max(0, pathDFS(node.left));
        int rightGain = Math.max(0, pathDFS(node.right));

        // Path passing through this node as highest root
        int currentPathSum = node.val + leftGain + rightGain;
        maxPathSumVal = Math.max(maxPathSumVal, currentPathSum);

        // Return maximum branch gain to parent
        return node.val + Math.max(leftGain, rightGain);
    }

    // ---------------------------------------------------------
    // LC 297: Serialize and Deserialize Binary Tree
    // ---------------------------------------------------------
    private static final String NULL_MARKER = "#";
    private static final String DELIMITER = ",";

    public static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        serializeHelper(root, sb);
        return sb.toString();
    }

    private static void serializeHelper(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append(NULL_MARKER).append(DELIMITER);
            return;
        }
        sb.append(node.val).append(DELIMITER);
        serializeHelper(node.left, sb);
        serializeHelper(node.right, sb);
    }

    public static TreeNode deserialize(String data) {
        if (data == null || data.isEmpty()) return null;
        Queue<String> queue = new LinkedList<>(Arrays.asList(data.split(DELIMITER)));
        return deserializeHelper(queue);
    }

    private static TreeNode deserializeHelper(Queue<String> queue) {
        if (queue.isEmpty()) return null;
        String valStr = queue.poll();
        if (valStr.equals(NULL_MARKER)) return null;

        TreeNode node = new TreeNode(Integer.parseInt(valStr));
        node.left = deserializeHelper(queue);
        node.right = deserializeHelper(queue);
        return node;
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 27: Advanced Binary Tree DSA Suite");
        System.out.println("==================================================");

        // Construct tree:
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);

        // Test 1: LC 543 Diameter
        int diameter = diameterOfBinaryTree(root);
        System.out.println("LC 543 (Diameter): " + diameter);
        assert diameter == 3 : "LC 543 Failed";

        // Test 2: LC 124 Max Path Sum
        // Tree: -10 -> 9, 20 (15, 7)
        TreeNode root2 = new TreeNode(-10);
        root2.left = new TreeNode(9);
        root2.right = new TreeNode(20);
        root2.right.left = new TreeNode(15);
        root2.right.right = new TreeNode(7);

        int maxSum = maxPathSum(root2);
        System.out.println("LC 124 (Max Path Sum): " + maxSum);
        assert maxSum == 42 : "LC 124 Failed";

        // Test 3: LC 297 Serialize & Deserialize
        String serialized = serialize(root);
        System.out.println("LC 297 Serialized: " + serialized);
        TreeNode reconstructed = deserialize(serialized);
        assert reconstructed != null && reconstructed.val == 1 : "LC 297 Root Val Mismatch";
        assert reconstructed.left.left.val == 4 : "LC 297 Leaf Val Mismatch";
        System.out.println("LC 297 Deserialization: Verified Successfully");

        System.out.println("\nAll Java Advanced Tree tests executed successfully! [OK]");
    }
}
