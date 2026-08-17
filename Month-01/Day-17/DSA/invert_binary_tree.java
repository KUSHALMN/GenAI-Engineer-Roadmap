import java.util.LinkedList;
import java.util.Queue;

public class invert_binary_tree {
    // LeetCode #226 - Invert Binary Tree
    // Approach: Recursive Depth-First Search (DFS) or Iterative BFS
    // Time Complexity: O(n) where n is the number of nodes
    // Space Complexity: O(h) where h is the height of the tree (call stack)

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

    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;

        TreeNode temp = root.left;
        root.left = invertTree(root.right);
        root.right = invertTree(temp);

        return root;
    }

    // Helper method to print tree in level-order
    public static void printLevelOrder(TreeNode root) {
        if (root == null) {
            System.out.println("[]");
            return;
        }
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        StringBuilder sb = new StringBuilder("[");
        while (!queue.isEmpty()) {
            TreeNode curr = queue.poll();
            if (curr != null) {
                sb.append(curr.val).append(", ");
                queue.offer(curr.left);
                queue.offer(curr.right);
            }
        }
        if (sb.length() > 1) sb.setLength(sb.length() - 2);
        sb.append("]");
        System.out.println(sb.toString());
    }

    public static void main(String[] args) {
        invert_binary_tree solution = new invert_binary_tree();

        // Construct tree: [4, 2, 7, 1, 3, 6, 9]
        TreeNode root = new TreeNode(4);
        root.left = new TreeNode(2, new TreeNode(1), new TreeNode(3));
        root.right = new TreeNode(7, new TreeNode(6), new TreeNode(9));

        System.out.print("Original Tree: ");
        printLevelOrder(root);

        TreeNode inverted = solution.invertTree(root);

        System.out.print("Inverted Tree: ");
        printLevelOrder(inverted);
    }
}
