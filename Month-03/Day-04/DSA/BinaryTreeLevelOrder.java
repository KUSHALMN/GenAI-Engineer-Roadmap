import java.util.*;

/**
 * Day 04 (Month 03) DSA: Binary Tree Breadth-First Search (BFS) & Level Order Traversal
 * - LeetCode 102: Binary Tree Level Order Traversal
 * - LeetCode 103: Binary Tree Zigzag Level Order Traversal
 * - LeetCode 199: Binary Tree Right Side View
 * 
 * Invariant:
 * Queue size at the beginning of each loop iteration precisely matches the number
 * of nodes on the current tree level.
 */
public class BinaryTreeLevelOrder {

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
    // LC 102: Binary Tree Level Order Traversal - O(N) Time, O(N) Space
    // -------------------------------------------------------------
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>(levelSize);

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                currentLevel.add(curr.val);

                if (curr.left != null) queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }
            result.add(currentLevel);
        }

        return result;
    }

    // -------------------------------------------------------------
    // LC 103: Binary Tree Zigzag Level Order Traversal - O(N) Time, O(N) Space
    // -------------------------------------------------------------
    public static List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        boolean leftToRight = true;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            LinkedList<Integer> currentLevel = new LinkedList<>();

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();

                if (leftToRight) {
                    currentLevel.addLast(curr.val);
                } else {
                    currentLevel.addFirst(curr.val);
                }

                if (curr.left != null) queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }

            result.add(currentLevel);
            leftToRight = !leftToRight;
        }

        return result;
    }

    // -------------------------------------------------------------
    // LC 199: Binary Tree Right Side View - O(N) Time, O(H) Space
    // -------------------------------------------------------------
    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                // Last element in this level is visible from the right
                if (i == levelSize - 1) {
                    result.add(curr.val);
                }

                if (curr.left != null) queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }
        }

        return result;
    }

    // -------------------------------------------------------------
    // Verification & Test Suite
    // -------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  Day 04 DSA: Tree BFS & Level Order Traversal  ");
        System.out.println("=================================================\n");

        // Construct Tree: [3, 9, 20, null, null, 15, 7]
        //       3
        //      / \
        //     9   20
        //        /  \
        //       15   7
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20, new TreeNode(15), new TreeNode(7));

        List<List<Integer>> levels = levelOrder(root);
        System.out.println("LC 102 Level Order: " + levels);
        assert levels.size() == 3;
        assert levels.get(0).equals(Arrays.asList(3));
        assert levels.get(1).equals(Arrays.asList(9, 20));
        assert levels.get(2).equals(Arrays.asList(15, 7));

        List<List<Integer>> zigzag = zigzagLevelOrder(root);
        System.out.println("LC 103 Zigzag Order: " + zigzag);
        assert zigzag.get(1).equals(Arrays.asList(20, 9));

        List<Integer> rightView = rightSideView(root);
        System.out.println("LC 199 Right Side View: " + rightView);
        assert rightView.equals(Arrays.asList(3, 20, 7));

        System.out.println("\nAll Day 04 Tree BFS test cases passed successfully!");
    }
}
