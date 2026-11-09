import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class MonotonicHistogram {
    public static int largestRectangleArea(int[] heights) {
        if (heights == null || heights.length == 0) return 0;
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && heights[stack.peek()] > h) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }

    public static int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] ans = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prev = stack.pop();
                ans[prev] = i - prev;
            }
            stack.push(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println("=== Monotonic Stack Verification ===");
        int[] h = {2, 1, 5, 6, 2, 3};
        int area = largestRectangleArea(h);
        System.out.println("LC 84 (Max Rectangle): " + area);
        assert area == 10 : "Expected 10";

        int[] temps = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] days = dailyTemperatures(temps);
        System.out.println("LC 739: " + Arrays.toString(days));
        assert days[0] == 1 && days[2] == 4 : "LC 739 failed";
        System.out.println("Monotonic stack passed!");
    }
}
