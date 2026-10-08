import java.util.*;

/**
 * Day 07 (Month 03) DSA: Kth Smallest Element in a BST (LeetCode 230)
 * 
 * Approaches:
 * 1. Recursive Inorder Traversal with early termination - O(H + K) time, O(H) space.
 * 2. Iterative Stack Traversal - O(H + K) time, O(H) space.
 * 3. Morris Inorder Traversal (Threaded Binary Tree) - O(N) time, O(1) auxiliary space!
 */
public class KthSmallestBST {

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
    // Approach 1: Iterative Inorder with Stack - O(H + K) Time, O(H) Space
    // -------------------------------------------------------------
    public static int kthSmallestStack(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;

        while (curr != null || !stack.isEmpty()) {
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            k--;
            if (k == 0) {
                return curr.val;
            }

            curr = curr.right;
        }

        throw new IllegalArgumentException("k is larger than tree size");
    }

    // -------------------------------------------------------------
    // Approach 2: Recursive Inorder with Counter State
    // -------------------------------------------------------------
    public static class RecursiveSolver {
        private int count = 0;
        private int result = -1;

        public int kthSmallest(TreeNode root, int k) {
            count = 0;
            result = -1;
            inorder(root, k);
            return result;
        }

        private void inorder(TreeNode node, int k) {
            if (node == null || result != -1) return;

            inorder(node.left, k);

            count++;
            if (count == k) {
                result = node.val;
                return;
            }

            inorder(node.right, k);
        }
    }

    // -------------------------------------------------------------
    // Approach 3: Morris Inorder Traversal - O(N) Time, O(1) Space!
    // -------------------------------------------------------------
    public static int kthSmallestMorris(TreeNode root, int k) {
        TreeNode curr = root;
        int count = 0;
        int result = -1;

        while (curr != null) {
            if (curr.left == null) {
                count++;
                if (count == k) result = curr.val;
                curr = curr.right;
            } else {
                // Find inorder predecessor
                TreeNode pred = curr.left;
                while (pred.right != null && pred.right != curr) {
                    pred = pred.right;
                }

                if (pred.right == null) {
                    // Create thread back to current
                    pred.right = curr;
                    curr = curr.left;
                } else {
                    // Break thread
                    pred.right = null;
                    count++;
                    if (count == k) result = curr.val;
                    curr = curr.right;
                }
            }
        }

        return result;
    }

    // -------------------------------------------------------------
    // Verification & Test Suite
    // -------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  Day 07 DSA: Kth Smallest Element in BST Tests  ");
        System.out.println("=================================================\n");

        // Construct BST: [5, 3, 6, 2, 4, null, null, 1]
        //          5
        //        /   \
        //       3     6
        //      / \
        //     2   4
        //    /
        //   1
        TreeNode n1 = new TreeNode(1);
        TreeNode n2 = new TreeNode(2, n1, null);
        TreeNode n4 = new TreeNode(4);
        TreeNode n3 = new TreeNode(3, n2, n4);
        TreeNode n6 = new TreeNode(6);
        TreeNode root = new TreeNode(5, n3, n6);

        // Sorted inorder order is: 1, 2, 3, 4, 5, 6
        for (int k = 1; k <= 6; k++) {
            int ansStack = kthSmallestStack(root, k);
            int ansRec = new RecursiveSolver().kthSmallest(root, k);
            int ansMorris = kthSmallestMorris(root, k);

            assert ansStack == k : "Mismatch in Stack approach for k=" + k;
            assert ansRec == k : "Mismatch in Recursive approach for k=" + k;
            assert ansMorris == k : "Mismatch in Morris approach for k=" + k;

            System.out.printf("k = %d -> %d [Stack: %d, Rec: %d, Morris: %d] -> PASSED%n",
                    k, k, ansStack, ansRec, ansMorris);
        }

        System.out.println("\nAll Day 07 Kth Smallest in BST tests passed successfully!");
    }
}
