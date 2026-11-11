package Month08.Day08;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Timed Set: Stacks & Queues
 * LC 739: Daily Temperatures - O(N) time with monotonic decreasing stack.
 */
public class StacksQueuesTimedSet {

    public static int[] dailyTemperatures(int[] temperatures) {
        int[] result = new int[temperatures.length];
        Deque<Integer> stack = new ArrayDeque<>(); // Indices of temperatures

        for (int i = 0; i < temperatures.length; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        return result;
    }

    public static void main(String[] args) {
        int[] temps = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] waitDays = dailyTemperatures(temps);
        assert waitDays[0] == 1;
        assert waitDays[2] == 4;

        System.out.println("Day 08 Stacks & Queues Timed Set verification passed.");
    }
}
