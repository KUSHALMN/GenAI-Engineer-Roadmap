package Month_09.Day_16.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 16: Timed DSA Problem Set — Monotonic Deque Sliding Window Maximum.
 * Focus: LeetCode 239 (Sliding Window Maximum) - O(N) Time, O(K) Space Monotonic Deque.
 */
public class SlidingWindowMaximumTimedSet {

    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];
        int n = nums.length;
        int[] result = new int[n - k + 1];
        int ri = 0;
        // Monotonic Deque storing indices of elements in non-increasing order of values
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            // 1. Evict indices outside the current window [i - k + 1 .. i]
            while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
                deque.pollFirst();
            }

            // 2. Remove elements from back that are smaller than the current element nums[i]
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
                deque.pollLast();
            }

            // 3. Add current index to back
            deque.offerLast(i);

            // 4. Record current window maximum once window reaches size k
            if (i >= k - 1) {
                result[ri++] = nums[deque.peekFirst()];
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] nums1 = {1, 3, -1, -3, 5, 3, 6, 7};
        int[] res1 = maxSlidingWindow(nums1, 3);
        int[] exp1 = {3, 3, 5, 5, 6, 7};
        assert res1.length == exp1.length : "Test 1 length failed";
        for (int i = 0; i < res1.length; i++) {
            assert res1[i] == exp1[i] : "Test 1 value mismatch at " + i;
        }

        int[] nums2 = {1};
        assert maxSlidingWindow(nums2, 1)[0] == 1 : "Test 2 Failed";

        int[] nums3 = {1, -1};
        int[] res3 = maxSlidingWindow(nums3, 1);
        assert res3[0] == 1 && res3[1] == -1 : "Test 3 Failed";

        System.out.println("Day 16 Sliding Window Maximum Timed Set verification passed.");
    }
}
