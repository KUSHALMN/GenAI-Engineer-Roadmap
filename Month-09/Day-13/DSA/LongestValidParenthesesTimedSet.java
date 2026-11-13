package Month_09.Day_13.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 13: Timed DSA Problem Set — Longest Valid Parentheses.
 * Focus: LeetCode 32 (Longest Valid Parentheses) - O(N) Time, O(1) Space Two-Pass & O(N) Stack.
 */
public class LongestValidParenthesesTimedSet {

    // LeetCode 32: Stack Approach - O(N) Time, O(N) Space
    public static int longestValidParenthesesStack(String s) {
        if (s == null || s.length() < 2) return 0;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1); // Base index for length calculation
        int maxLen = 0;

        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else {
                stack.pop();
                if (stack.isEmpty()) {
                    stack.push(i); // Reset base index to current unmatched ')'
                } else {
                    maxLen = Math.max(maxLen, i - stack.peek());
                }
            }
        }
        return maxLen;
    }

    // LeetCode 32: Two-Pass Counter Approach - O(N) Time, O(1) Space
    public static int longestValidParenthesesTwoPass(String s) {
        if (s == null || s.length() < 2) return 0;
        int left = 0, right = 0, maxLen = 0;

        // Left to Right scan
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') left++;
            else right++;

            if (left == right) {
                maxLen = Math.max(maxLen, 2 * right);
            } else if (right > left) {
                left = right = 0;
            }
        }

        left = right = 0;
        // Right to Left scan
        for (int i = s.length() - 1; i >= 0; i--) {
            if (s.charAt(i) == '(') left++;
            else right++;

            if (left == right) {
                maxLen = Math.max(maxLen, 2 * left);
            } else if (left > right) {
                left = right = 0;
            }
        }
        return maxLen;
    }

    public static void main(String[] args) {
        assert longestValidParenthesesStack("(()") == 2 : "Test 1 Failed";
        assert longestValidParenthesesStack(")()())") == 4 : "Test 2 Failed";
        assert longestValidParenthesesStack("") == 0 : "Test 3 Failed";
        assert longestValidParenthesesStack("()(())") == 6 : "Test 4 Failed";

        assert longestValidParenthesesTwoPass("(()") == 2 : "TwoPass Test 1 Failed";
        assert longestValidParenthesesTwoPass(")()())") == 4 : "TwoPass Test 2 Failed";
        assert longestValidParenthesesTwoPass("()(())") == 6 : "TwoPass Test 4 Failed";

        System.out.println("Day 13 Longest Valid Parentheses Timed Set verification passed.");
    }
}
