package Month_09.Day_15.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 15: Timed DSA Problem Set — Maximal Rectangle in 2D Binary Matrix.
 * Focus: LeetCode 85 (Maximal Rectangle) - O(R * C) Time, O(C) Space.
 */
public class MaximalRectangleTimedSet {

    public static int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return 0;
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (matrix[r][c] == '1') {
                    heights[c]++;
                } else {
                    heights[c] = 0; // Reset consecutive height on 0
                }
            }
            maxArea = Math.max(maxArea, largestRectangleHistogram(heights));
        }
        return maxArea;
    }

    private static int largestRectangleHistogram(int[] heights) {
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

    public static void main(String[] args) {
        char[][] matrix1 = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        assert maximalRectangle(matrix1) == 6 : "Test 1 Failed";

        char[][] matrix2 = {{'0'}};
        assert maximalRectangle(matrix2) == 0 : "Test 2 Failed";

        char[][] matrix3 = {{'1'}};
        assert maximalRectangle(matrix3) == 1 : "Test 3 Failed";

        System.out.println("Day 15 Maximal Rectangle Timed Set verification passed.");
    }
}
