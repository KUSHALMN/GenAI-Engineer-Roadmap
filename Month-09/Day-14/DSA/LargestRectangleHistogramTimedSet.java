package Month_09.Day_14.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 14: Timed DSA Problem Set — Monotonic Stack Largest Rectangle in Histogram.
 * Focus: LeetCode 84 (Largest Rectangle in Histogram) - O(N) Time, O(N) Space Monotonic Stack.
 */
public class LargestRectangleHistogramTimedSet {

    public static int largestRectangleArea(int[] heights) {
        if (heights == null || heights.length == 0) return 0;
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            // Append virtual bar of height 0 at index n to flush the stack
            int currentHeight = (i == n) ? 0 : heights[i];

            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }

    public static void main(String[] args) {
        assert largestRectangleArea(new int[]{2, 1, 5, 6, 2, 3}) == 10 : "Test 1 Failed";
        assert largestRectangleArea(new int[]{2, 4}) == 4 : "Test 2 Failed";
        assert largestRectangleArea(new int[]{1}) == 1 : "Test 3 Failed";
        assert largestRectangleArea(new int[]{6, 2, 5, 4, 5, 1, 6}) == 12 : "Test 4 Failed";

        System.out.println("Day 14 Largest Rectangle in Histogram Timed Set verification passed.");
    }
}
