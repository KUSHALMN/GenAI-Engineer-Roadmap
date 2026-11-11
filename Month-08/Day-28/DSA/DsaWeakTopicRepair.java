package Month_08.Day_28.DSA;

import java.util.*;

/**
 * Day 28: Timed DSA Problem Set — Weak Topic Repair (Hard Matrix DP & Tree Serialization).
 * Focus: LeetCode 85 (Maximal Rectangle) & LeetCode 297 (Serialize and Deserialize Binary Tree).
 */
public class DsaWeakTopicRepair {

    // LeetCode 85: Maximal Rectangle - O(R * C) Time using Monotonic Histogram Stack
    public static int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return 0;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;

        for (char[] row : matrix) {
            for (int j = 0; j < cols; j++) {
                if (row[j] == '1') {
                    heights[j]++;
                } else {
                    heights[j] = 0;
                }
            }
            maxArea = Math.max(maxArea, largestRectangleInHistogram(heights));
        }
        return maxArea;
    }

    private static int largestRectangleInHistogram(int[] heights) {
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && h < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }

    // LeetCode 297: Codec for Binary Tree
    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    public static class Codec {
        public String serialize(TreeNode root) {
            StringBuilder sb = new StringBuilder();
            buildString(root, sb);
            return sb.toString();
        }

        private void buildString(TreeNode node, StringBuilder sb) {
            if (node == null) {
                sb.append("#," );
            } else {
                sb.append(node.val).append(",");
                buildString(node.left, sb);
                buildString(node.right, sb);
            }
        }

        public TreeNode deserialize(String data) {
            Deque<String> nodes = new ArrayDeque<>(Arrays.asList(data.split(",")));
            return buildTree(nodes);
        }

        private TreeNode buildTree(Deque<String> nodes) {
            String val = nodes.poll();
            if (val == null || val.equals("#")) return null;
            TreeNode node = new TreeNode(Integer.parseInt(val));
            node.left = buildTree(nodes);
            node.right = buildTree(nodes);
            return node;
        }
    }

    public static void main(String[] args) {
        // LC 85 tests
        char[][] matrix = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        assert maximalRectangle(matrix) == 6 : "Maximal Rectangle failed";

        // LC 297 tests
        Codec codec = new Codec();
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.right.left = new TreeNode(4);
        root.right.right = new TreeNode(5);

        String serialized = codec.serialize(root);
        TreeNode deserialized = codec.deserialize(serialized);
        assert codec.serialize(deserialized).equals(serialized) : "Tree serialization mismatch";

        System.out.println("Day 28 DSA Weak Topic Repair (LC 85 & LC 297) verification passed.");
    }
}
