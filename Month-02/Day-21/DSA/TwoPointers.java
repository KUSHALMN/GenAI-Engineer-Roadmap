import java.util.Arrays;

/**
 * Day 21 DSA — Two Pointers Patterns
 *
 * Problems:
 *   1. LC 167 - Two Sum II (sorted array)
 *   2. LC 15  - 3Sum
 *   3. LC 11  - Container With Most Water
 *
 * Pattern: Two pointers from both ends, converge based on condition.
 * Time: O(n) or O(n^2) | Space: O(1)
 */
public class TwoPointers {

    // LC 167 - Two Sum II
    public int[] twoSum(int[] numbers, int target) {
        int l = 0, r = numbers.length - 1;
        while (l < r) {
            int sum = numbers[l] + numbers[r];
            if (sum == target) return new int[]{l + 1, r + 1};
            else if (sum < target) l++;
            else r--;
        }
        return new int[]{};
    }

    // LC 15 - 3Sum
    public java.util.List<java.util.List<Integer>> threeSum(int[] nums) {
        java.util.List<java.util.List<Integer>> res = new java.util.ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return res;
    }

    // LC 11 - Container With Most Water
    public int maxArea(int[] height) {
        int l = 0, r = height.length - 1, max = 0;
        while (l < r) {
            max = Math.max(max, Math.min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return max;
    }

    public static void main(String[] args) {
        TwoPointers sol = new TwoPointers();

        // LC 167
        System.out.println(Arrays.toString(sol.twoSum(new int[]{2, 7, 11, 15}, 9))); // [1, 2]

        // LC 15
        System.out.println(sol.threeSum(new int[]{-1, 0, 1, 2, -1, -4})); // [[-1,-1,2],[-1,0,1]]

        // LC 11
        System.out.println(sol.maxArea(new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7})); // 49
    }
}
