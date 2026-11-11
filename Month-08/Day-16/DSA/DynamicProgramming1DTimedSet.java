package Month_08.Day_16.DSA;

/**
 * Day 16: Timed DSA Problem Set — 1D Dynamic Programming.
 * Focus: LeetCode 198 (House Robber) & LeetCode 70 (Climbing Stairs).
 */
public class DynamicProgramming1DTimedSet {

    // LeetCode 198: House Robber - O(n) Time, O(1) Space
    public static int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];

        int prev2 = 0;
        int prev1 = 0;
        for (int num : nums) {
            int current = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }

    // LeetCode 70: Climbing Stairs - O(n) Time, O(1) Space
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int next = a + b;
            a = b;
            b = next;
        }
        return b;
    }

    public static void main(String[] args) {
        // LC 198 tests
        assert rob(new int[]{1, 2, 3, 1}) == 4 : "Test 1 Failed";
        assert rob(new int[]{2, 7, 9, 3, 1}) == 12 : "Test 2 Failed";
        assert rob(new int[]{2, 1, 1, 2}) == 4 : "Test 3 Failed";

        // LC 70 tests
        assert climbStairs(2) == 2 : "LC 70 Test 1 Failed";
        assert climbStairs(3) == 3 : "LC 70 Test 2 Failed";
        assert climbStairs(5) == 8 : "LC 70 Test 3 Failed";

        System.out.println("Day 16 1D Dynamic Programming Timed Set verification passed.");
    }
}
