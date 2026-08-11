import java.util.Stack;
import java.util.Arrays;

public class daily_temperatures {
    // LeetCode #739 - Daily Temperatures
    // Approach: Monotonic decreasing stack O(n)
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int idx = stack.pop();
                result[idx] = i - idx;
            }
            stack.push(i);
        }
        return result;
    }

    public static void main(String[] args) {
        daily_temperatures sol = new daily_temperatures();
        System.out.println(Arrays.toString(sol.dailyTemperatures(new int[]{73,74,75,71,69,72,76,73})));  // [1,1,4,2,1,1,0,0]
        System.out.println(Arrays.toString(sol.dailyTemperatures(new int[]{30,40,50,60})));               // [1,1,1,0]
    }
}
