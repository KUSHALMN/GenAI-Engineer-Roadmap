import java.util.*;

/**
 * Problem: Serialize and Deserialize Binary Tree (LeetCode 297 - Hard / FAANG Classic)
 * 
 * Design an algorithm to serialize and deserialize a binary tree.
 * There is no restriction on how your serialization/deserialization algorithm should work.
 * You just need to ensure that a binary tree can be serialized to a string
 * and this string can be deserialized to the original tree structure.
 * 
 * Approaches:
 * 1. Breadth-First Search (BFS / Level Order):
 *    - Serialize using a Queue, separating values with commas and representing nulls with "#" or "null".
 *    - Deserialize using a Queue to reconstruct parent-child relationships layer by layer.
 *    - Time Complexity: O(N)
 *    - Space Complexity: O(N)
 * 
 * 2. Preorder Traversal (DFS with Sentinels):
 *    - Root -> Left -> Right with null marker.
 */
public class serialize_deserialize_binary_tree {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int x) { val = x; }
    }

    private static final String NULL_NODE = "null";
    private static final String DELIMITER = ",";

    // ==========================================
    // Approach 1: BFS Level-Order Serialization
    // ==========================================
    public static String serialize(TreeNode root) {
        if (root == null) return "";

        StringBuilder sb = new StringBuilder();
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            TreeNode curr = queue.poll();
            if (curr == null) {
                sb.append(NULL_NODE).append(DELIMITER);
            } else {
                sb.append(curr.val).append(DELIMITER);
                queue.offer(curr.left);
                queue.offer(curr.right);
            }
        }

        // Delete trailing delimiter
        if (sb.length() > 0) {
            sb.setLength(sb.length() - 1);
        }
        return sb.toString();
    }

    // ==========================================
    // Approach 1: BFS Level-Order Deserialization
    // ==========================================
    public static TreeNode deserialize(String data) {
        if (data == null || data.trim().isEmpty()) return null;

        String[] tokens = data.split(DELIMITER);
        if (tokens[0].equals(NULL_NODE)) return null;

        TreeNode root = new TreeNode(Integer.parseInt(tokens[0]));
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        int idx = 1;
        while (!queue.isEmpty() && idx < tokens.length) {
            TreeNode parent = queue.poll();

            // Process left child
            if (!tokens[idx].equals(NULL_NODE)) {
                TreeNode leftChild = new TreeNode(Integer.parseInt(tokens[idx]));
                parent.left = leftChild;
                queue.offer(leftChild);
            }
            idx++;

            // Process right child
            if (idx < tokens.length && !tokens[idx].equals(NULL_NODE)) {
                TreeNode rightChild = new TreeNode(Integer.parseInt(tokens[idx]));
                parent.right = rightChild;
                queue.offer(rightChild);
            }
            idx++;
        }

        return root;
    }

    // Helper: Compare two trees for structural & value equality
    public static boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null) return false;
        return (p.val == q.val) && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 297: Serialize / Deserialize Binary Tree");
        System.out.println("=================================================");

        // Tree 1: [1, 2, 3, null, null, 4, 5]
        TreeNode root1 = new TreeNode(1);
        root1.left = new TreeNode(2);
        root1.right = new TreeNode(3);
        root1.right.left = new TreeNode(4);
        root1.right.right = new TreeNode(5);

        String serialized1 = serialize(root1);
        System.out.println("Serialized Tree 1: " + serialized1);

        TreeNode deserialized1 = deserialize(serialized1);
        boolean matches1 = isSameTree(root1, deserialized1);
        System.out.println("Round-trip equality check -> Expected true: " + matches1);
        assert matches1 : "Failed Round-trip Test 1";

        // Tree 2: Empty tree
        String serialized2 = serialize(null);
        TreeNode deserialized2 = deserialize(serialized2);
        assert deserialized2 == null : "Failed Empty Tree Test 2";

        // Tree 3: Single node
        TreeNode root3 = new TreeNode(42);
        String serialized3 = serialize(root3);
        TreeNode deserialized3 = deserialize(serialized3);
        assert isSameTree(root3, deserialized3) : "Failed Single Node Test 3";

        System.out.println("\n✅ All Binary Tree Codec tests passed successfully!");
    }
}
