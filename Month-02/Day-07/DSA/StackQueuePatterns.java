import java.util.*;

/**
 * Stack, Queue & Monotonic Stack Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 20 - Valid Parentheses -> O(N) time, O(N) space
 *   2. LeetCode 739 - Daily Temperatures (Monotonic Stack) -> O(N) time, O(N) space
 *   3. LeetCode 155 - Min Stack -> O(1) time all operations
 */
public class StackQueuePatterns {

    /**
     * LC 20: Valid Parentheses
     */
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }

    /**
     * LC 739: Daily Temperatures (Monotonic Decreasing Stack of indices)
     */
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>(); // stores indices

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        return result;
    }

    /**
     * LC 155: Min Stack implementation
     */
    public static class MinStack {
        private Deque<Integer> stack = new ArrayDeque<>();
        private Deque<Integer> minStack = new ArrayDeque<>();

        public void push(int val) {
            stack.push(val);
            if (minStack.isEmpty() || val <= minStack.peek()) {
                minStack.push(val);
            }
        }

        public void pop() {
            if (!stack.isEmpty()) {
                int val = stack.pop();
                if (val == minStack.peek()) {
                    minStack.pop();
                }
            }
        }

        public int top() {
            return stack.peek();
        }

        public int getMin() {
            return minStack.peek();
        }
    }

    public static void main(String[] args) {
        StackQueuePatterns sq = new StackQueuePatterns();

        // 1. Valid Parentheses
        System.out.println("Valid Parentheses '()[]{}': " + sq.isValid("()[]{}")); // true
        System.out.println("Valid Parentheses '(]': " + sq.isValid("(]")); // false

        // 2. Daily Temperatures
        int[] temps = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] daily = sq.dailyTemperatures(temps);
        System.out.println("Daily Temperatures: " + Arrays.toString(daily)); // [1, 1, 4, 2, 1, 1, 0, 0]

        // 3. Min Stack
        MinStack ms = new MinStack();
        ms.push(-2);
        ms.push(0);
        ms.push(-3);
        System.out.println("MinStack getMin: " + ms.getMin()); // -3
        ms.pop();
        System.out.println("MinStack top: " + ms.top());       // 0
        System.out.println("MinStack getMin: " + ms.getMin()); // -2
    }
}
