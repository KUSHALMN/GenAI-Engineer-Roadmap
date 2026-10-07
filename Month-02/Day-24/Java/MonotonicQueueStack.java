import java.util.*;

/**
 * Day 24 DSA: Monotonic Queue & Stack Patterns
 * - LeetCode 239: Sliding Window Maximum (Monotonic Decreasing Deque)
 * - LeetCode 739: Daily Temperatures (Monotonic Decreasing Stack)
 * - LeetCode 496: Next Greater Element I (Monotonic Stack + Hash Table)
 */
public class MonotonicQueueStack {

    /**
     * LC 239: Sliding Window Maximum
     * Time Complexity: O(N) — each element added and removed at most once
     * Space Complexity: O(K) — deque stores at most k indices
     */
    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];
        int n = nums.length;
        int[] result = new int[n - k + 1];
        int ri = 0;

        // Deque stores array indices in strictly decreasing order of their values
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            // 1. Remove indices outside of current sliding window [i - k + 1, i]
            while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
                deque.pollFirst();
            }

            // 2. Maintain decreasing order: remove smaller elements from back
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
                deque.pollLast();
            }

            // 3. Add current element's index
            deque.offerLast(i);

            // 4. Record current window maximum once first window of size k is formed
            if (i >= k - 1) {
                result[ri++] = nums[deque.peekFirst()];
            }
        }
        return result;
    }

    /**
     * LC 739: Daily Temperatures
     * Return array answer where answer[i] is number of days until warmer temperature.
     * Time Complexity: O(N)
     * Space Complexity: O(N)
     */
    public static int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];
        Deque<Integer> stack = new ArrayDeque<>(); // stores indices of temperatures

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prevDay = stack.pop();
                answer[prevDay] = i - prevDay;
            }
            stack.push(i);
        }
        return answer;
    }

    /**
     * LC 496: Next Greater Element I
     * Time Complexity: O(N + M)
     * Space Complexity: O(N)
     */
    public static int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> nextGreater = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();

        for (int num : nums2) {
            while (!stack.isEmpty() && stack.peek() < num) {
                nextGreater.put(stack.pop(), num);
            }
            stack.push(num);
        }

        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            result[i] = nextGreater.getOrDefault(nums1[i], -1);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 24: Monotonic Queue & Stack DSA Suite");
        System.out.println("==================================================");

        // Test 1: Sliding Window Maximum
        int[] nums1 = {1, 3, -1, -3, 5, 3, 6, 7};
        int k1 = 3;
        int[] maxWin = maxSlidingWindow(nums1, k1);
        System.out.println("LC 239 (Sliding Window Max): " + Arrays.toString(maxWin));
        assert Arrays.equals(maxWin, new int[]{3, 3, 5, 5, 6, 7}) : "Test 1 Failed";

        // Test 2: Daily Temperatures
        int[] temps = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] daysToWarmer = dailyTemperatures(temps);
        System.out.println("LC 739 (Daily Temperatures): " + Arrays.toString(daysToWarmer));
        assert Arrays.equals(daysToWarmer, new int[]{1, 1, 4, 2, 1, 1, 0, 0}) : "Test 2 Failed";

        // Test 3: Next Greater Element
        int[] qNums1 = {4, 1, 2};
        int[] qNums2 = {1, 3, 4, 2};
        int[] nge = nextGreaterElement(qNums1, qNums2);
        System.out.println("LC 496 (Next Greater Element): " + Arrays.toString(nge));
        assert Arrays.equals(nge, new int[]{-1, 3, -1}) : "Test 3 Failed";

        System.out.println("\nAll Java Monotonic tests executed successfully! [OK]");
    }
}
