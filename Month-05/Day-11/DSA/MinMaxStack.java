import java.util.*;

/**
 * Day 11: Data Structure Design — MinStack with O(1) Operations
 * Supports push, pop, top, and retrieving the minimum element in O(1) time.
 */
public class MinMaxStack {

    private final Deque<Integer> stack = new ArrayDeque<>();
    private final Deque<Integer> minStack = new ArrayDeque<>();

    public void push(int val) {
        stack.push(val);
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }
    }

    public void pop() {
        if (stack.isEmpty()) return;
        int val = stack.pop();
        if (val == minStack.peek()) {
            minStack.pop();
        }
    }

    public int top() { return stack.peek(); }
    public int getMin() { return minStack.peek(); }

    public static void main(String[] args) {
        MinMaxStack s = new MinMaxStack();
        s.push(-2);
        s.push(0);
        s.push(-3);
        assert s.getMin() == -3;
        s.pop();
        assert s.top() == 0;
        assert s.getMin() == -2;
        System.out.println("Day 11 DSA MinMaxStack verification passed!");
    }
}
