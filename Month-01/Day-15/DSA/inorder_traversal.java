import java.util.ArrayList;
import java.util.List;

public class inorder_traversal {
    // LeetCode #94 - Binary Tree Inorder Traversal
    // Approach: DFS recursion O(n)

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        dfs(root, result);
        return result;
    }

    private void dfs(TreeNode node, List<Integer> result) {
        if (node == null) return;
        dfs(node.left, result);
        result.add(node.val);
        dfs(node.right, result);
    }

    public static void main(String[] args) {
        inorder_traversal sol = new inorder_traversal();

        TreeNode root = new TreeNode(1);
        root.right = new TreeNode(2);
        root.right.left = new TreeNode(3);

        System.out.println(sol.inorderTraversal(root));  // [1, 3, 2]
    }
}
