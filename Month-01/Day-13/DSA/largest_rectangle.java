import java.util.Stack;

public class largest_rectangle {
    // LeetCode #84 - Largest Rectangle in Histogram
    // Approach: Monotonic increasing stack O(n)
    public int largestRectangleArea(int[] heights) {
        Stack<Integer> stack = new Stack<>();
        int maxArea = 0;
        int n = heights.length;

        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && h < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }

    public static void main(String[] args) {
        largest_rectangle sol = new largest_rectangle();
        System.out.println(sol.largestRectangleArea(new int[]{2,1,5,6,2,3}));  // 10
        System.out.println(sol.largestRectangleArea(new int[]{2,4}));           // 4
    }
}
