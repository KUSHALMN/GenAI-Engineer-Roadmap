package Month_08.Day_27.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 27: Timed DSA Problem Set — Monotonic Stack & Edit Distance.
 * Focus: LeetCode 84 (Largest Rectangle in Histogram) & LeetCode 72 (Edit Distance).
 */
public class AlgorithmCommunicationMock {

    // LeetCode 84: Largest Rectangle in Histogram - O(N) Time, O(N) Space Monotonic Stack
    public static int largestRectangleArea(int[] heights) {
        if (heights == null || heights.length == 0) return 0;
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            int currentHeight = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int h = heights[stack.pop()];
                int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
                maxArea = Math.max(maxArea, h * width);
            }
            stack.push(i);
        }
        return maxArea;
    }

    // LeetCode 72: Edit Distance - O(M*N) Time, O(min(M,N)) Space
    public static int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[] dp = new int[n + 1];
        for (int j = 0; j <= n; j++) dp[j] = j;

        for (int i = 1; i <= m; i++) {
            int prevDiag = dp[0];
            dp[0] = i;
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[j] = prevDiag;
                } else {
                    dp[j] = 1 + Math.min(prevDiag, Math.min(dp[j], dp[j - 1]));
                }
                prevDiag = temp;
            }
        }
        return dp[n];
    }

    public static void main(String[] args) {
        // LC 84 tests
        assert largestRectangleArea(new int[]{2, 1, 5, 6, 2, 3}) == 10 : "LC 84 Test 1 Failed";
        assert largestRectangleArea(new int[]{2, 4}) == 4 : "LC 84 Test 2 Failed";

        // LC 72 tests
        assert minDistance("horse", "ros") == 3 : "LC 72 Test 1 Failed";
        assert minDistance("intention", "execution") == 5 : "LC 72 Test 2 Failed";

        System.out.println("Day 27 Algorithm Communication Mock (LC 84 & LC 72) verification passed.");
    }
}
