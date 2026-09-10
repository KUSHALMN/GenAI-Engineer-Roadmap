/**
 * LeetCode 198 - House Robber
 * Topic: Dynamic Programming (1D DP / Space-Optimized)
 *
 * Problem: Given an array of non-negative integers representing money in each
 * house, return the max amount you can rob without robbing two adjacent houses.
 *
 * Recurrence:
 *   dp[i] = max(dp[i-1], dp[i-2] + nums[i])
 *
 * Space Optimization: Only need prev2 and prev1, not full dp array.
 *
 * Time:  O(n)
 * Space: O(1)
 */
public class HouseRobber {

    public int rob(int[] nums) {
        if (nums.length == 1) return nums[0];

        int prev2 = 0, prev1 = 0;
        for (int num : nums) {
            int curr = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    // LC 213 - House Robber II (circular array)
    public int robCircular(int[] nums) {
        if (nums.length == 1) return nums[0];
        return Math.max(
            robRange(nums, 0, nums.length - 2),
            robRange(nums, 1, nums.length - 1)
        );
    }

    private int robRange(int[] nums, int start, int end) {
        int prev2 = 0, prev1 = 0;
        for (int i = start; i <= end; i++) {
            int curr = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    public static void main(String[] args) {
        HouseRobber sol = new HouseRobber();

        // LC 198 tests
        System.out.println(sol.rob(new int[]{1, 2, 3, 1}));        // 4  (1+3)
        System.out.println(sol.rob(new int[]{2, 7, 9, 3, 1}));     // 12 (2+9+1)
        System.out.println(sol.rob(new int[]{5}));                  // 5
        System.out.println(sol.rob(new int[]{2, 1}));               // 2

        // LC 213 tests (circular)
        System.out.println(sol.robCircular(new int[]{2, 3, 2}));    // 3
        System.out.println(sol.robCircular(new int[]{1, 2, 3, 1})); // 4
    }
}
