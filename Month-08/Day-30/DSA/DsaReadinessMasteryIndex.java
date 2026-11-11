package Month_08.Day_30.DSA;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Day 30: Timed DSA Problem Set — DSA Readiness Mastery Index.
 * Focus: LeetCode 41 (First Missing Positive) & LeetCode 239 (Sliding Window Maximum).
 */
public class DsaReadinessMasteryIndex {

    // LeetCode 41: First Missing Positive - O(N) Time, O(1) Space (Index Hash / Cyclic Sort)
    public static int firstMissingPositive(int[] nums) {
        if (nums == null || nums.length == 0) return 1;
        int n = nums.length;

        for (int i = 0; i < n; i++) {
            while (nums[i] > 0 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int temp = nums[nums[i] - 1];
                nums[nums[i] - 1] = nums[i];
                nums[i] = temp;
            }
        }

        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) {
                return i + 1;
            }
        }
        return n + 1;
    }

    // LeetCode 239: Sliding Window Maximum - O(N) Time, O(k) Space Monotonic Deque
    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];
        int n = nums.length;
        int[] result = new int[n - k + 1];
        int ri = 0;
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            // Remove elements outside current window
            while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
                deque.pollFirst();
            }
            // Remove elements smaller than current element from back
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
                deque.pollLast();
            }
            deque.offerLast(i);

            if (i >= k - 1) {
                result[ri++] = nums[deque.peekFirst()];
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // LC 41 tests
        assert firstMissingPositive(new int[]{1, 2, 0}) == 3 : "LC 41 Test 1 Failed";
        assert firstMissingPositive(new int[]{3, 4, -1, 1}) == 2 : "LC 41 Test 2 Failed";
        assert firstMissingPositive(new int[]{7, 8, 9, 11, 12}) == 1 : "LC 41 Test 3 Failed";

        // LC 239 tests
        int[] nums = {1, 3, -1, -3, 5, 3, 6, 7};
        int[] maxes = maxSlidingWindow(nums, 3);
        int[] expected = {3, 3, 5, 5, 6, 7};
        assert maxes.length == expected.length : "LC 239 Length mismatch";
        for (int i = 0; i < maxes.length; i++) {
            assert maxes[i] == expected[i] : "LC 239 Value mismatch at " + i;
        }

        System.out.println("Day 30 DSA Readiness Mastery Index (LC 41 & LC 239) verification passed.");
    }
}
