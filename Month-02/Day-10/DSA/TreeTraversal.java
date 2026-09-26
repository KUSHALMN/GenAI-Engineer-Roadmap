import java.util.*;

/**
 * Binary Tree Traversals in Java
 *
 * Problems Covered:
 *   1. LeetCode 102 - Binary Tree Level Order Traversal (BFS) -> O(N) time, O(N) space
 *   2. LeetCode 104 - Maximum Depth of Binary Tree (DFS) -> O(N) time, O(H) space
 *   3. LeetCode 226 - Invert Binary Tree -> O(N) time, O(H) space
 */
public class TreeTraversal {

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
     * LC 102: Level Order Traversal (BFS using Queue)
     */
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();

            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                currentLevel.add(node.val);
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(currentLevel);
        }
        return result;
    }

    /**
     * LC 104: Maximum Depth of Binary Tree
     */
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }

    /**
     * LC 226: Invert Binary Tree
     */
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;

        TreeNode temp = root.left;
        root.left = root.right;
        root.right = temp;

        invertTree(root.left);
        invertTree(root.right);
        return root;
    }

    public static void main(String[] args) {
        TreeTraversal tt = new TreeTraversal();

        // Construct tree:
        //       3
        //      / \
        //     9   20
        //        /  \
        //       15   7
        TreeNode root = new TreeNode(3,
            new TreeNode(9),
            new TreeNode(20, new TreeNode(15), new TreeNode(7))
        );

        // 1. Level order
        List<List<Integer>> levels = tt.levelOrder(root);
        System.out.println("LC 102 Level Order: " + levels); // [[3], [9, 20], [15, 7]]

        // 2. Max depth
        int depth = tt.maxDepth(root);
        System.out.println("LC 104 Max Depth: " + depth); // 3

        // 3. Invert tree
        TreeNode inv = tt.invertTree(root);
        List<List<Integer>> invLevels = tt.levelOrder(inv);
        System.out.println("LC 226 Inverted Levels: " + invLevels); // [[3], [20, 9], [7, 15]]
    }
}
