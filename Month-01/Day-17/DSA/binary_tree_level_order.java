import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class binary_tree_level_order {
    // LeetCode #102 - Binary Tree Level Order Traversal
    // Approach: Breadth-First Search (BFS) using a Queue
    // Time Complexity: O(n) where n is the number of nodes
    // Space Complexity: O(n) for queue storage in worst case (broadest level)

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

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

    public static void main(String[] args) {
        binary_tree_level_order solution = new binary_tree_level_order();

        // Construct tree: [3, 9, 20, null, null, 15, 7]
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20, new TreeNode(15), new TreeNode(7));

        List<List<Integer>> levels = solution.levelOrder(root);
        System.out.println("Level Order Traversal: " + levels);
        // Output: [[3], [9, 20], [15, 7]]
    }
}
