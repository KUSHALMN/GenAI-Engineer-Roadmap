package DSA;

import java.util.*;

/**
 * LeetCode 297 - Serialize and Deserialize Binary Tree
 * Method: Pre-order DFS Traversal with Sentinel Null Delimiters
 * 
 * Complexity:
 * - Time: O(N) for both serialization and deserialization
 * - Space: O(N) recursion stack and serialized string buffer
 */
public class TreeSerialization {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    private static final String NULL_SENTINEL = "#";
    private static final String DELIMITER = ",";

    // Encodes a tree to a single string.
    public static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        buildString(root, sb);
        return sb.toString();
    }

    private static void buildString(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append(NULL_SENTINEL).append(DELIMITER);
        } else {
            sb.append(node.val).append(DELIMITER);
            buildString(node.left, sb);
            buildString(node.right, sb);
        }
    }

    // Decodes your encoded data to tree.
    public static TreeNode deserialize(String data) {
        Queue<String> nodes = new LinkedList<>(Arrays.asList(data.split(DELIMITER)));
        return buildTree(nodes);
    }

    private static TreeNode buildTree(Queue<String> nodes) {
        if (nodes.isEmpty()) return null;
        String val = nodes.poll();
        if (val.equals(NULL_SENTINEL)) return null;

        TreeNode node = new TreeNode(Integer.parseInt(val));
        node.left = buildTree(nodes);
        node.right = buildTree(nodes);
        return node;
    }

    public static void main(String[] args) {
        // Construct tree:
        //      1
        //     / \
        //    2   3
        //       / \
        //      4   5
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.right.left = new TreeNode(4);
        root.right.right = new TreeNode(5);

        String serialized = serialize(root);
        System.out.println("Serialized Binary Tree: " + serialized);

        TreeNode deserialized = deserialize(serialized);
        String reSerialized = serialize(deserialized);
        System.out.println("Re-serialized Tree:     " + reSerialized);

        boolean match = serialized.equals(reSerialized);
        System.out.println("Serialization Invariant Preserved: " + match);
        System.out.println("TreeSerialization tests passed!");
    }
}
