import java.util.*;

/**
 * Day 09: Dynamic Programming — House Robber
 * Problem: Determine the maximum amount of money you can rob tonight without alerting the police
 * (cannot rob two adjacent houses).
 *
 * Algorithm:
 * - Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
 * - Space optimized: track only previous two values (prev1, prev2).
 *
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 */
public class HouseRobberDP {

    public int rob(int[] nums) {
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

    public static void main(String[] args) {
        HouseRobberDP solver = new HouseRobberDP();
        int[] houses = {2, 7, 9, 3, 1};
        int maxLoot = solver.rob(houses);

        System.out.println("Maximum loot for [2, 7, 9, 3, 1]: " + maxLoot);
        assert maxLoot == 12 : "Expected 12 (rob house 1, 3, and 5: 2 + 9 + 1 = 12)";
        System.out.println("Day 09 DSA HouseRobberDP verification passed!");
    }
}
