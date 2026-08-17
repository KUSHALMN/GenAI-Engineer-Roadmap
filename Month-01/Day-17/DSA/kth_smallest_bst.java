import java.util.Stack;

public class kth_smallest_bst {
    // LeetCode #230 - Kth Smallest Element in a BST
    // Approach: In-order traversal yields elements in sorted ascending order.
    // Iterative Stack traversal stops early at the k-th element.
    // Time Complexity: O(h + k) where h is tree height
    // Space Complexity: O(h) for recursion/stack space

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

    public int kthSmallest(TreeNode root, int k) {
        Stack<TreeNode> stack = new Stack<>();
        TreeNode curr = root;

        while (curr != null || !stack.isEmpty()) {
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            k--;
            if (k == 0) return curr.val;

            curr = curr.right;
        }

        return -1;
    }

    public static void main(String[] args) {
        kth_smallest_bst solution = new kth_smallest_bst();

        // BST: [3, 1, 4, null, 2]
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(1, null, new TreeNode(2));
        root.right = new TreeNode(4);

        System.out.println("1st smallest element (k=1): " + solution.kthSmallest(root, 1)); // 1
        System.out.println("2nd smallest element (k=2): " + solution.kthSmallest(root, 2)); // 2
        System.out.println("3rd smallest element (k=3): " + solution.kthSmallest(root, 3)); // 3
    }
}
