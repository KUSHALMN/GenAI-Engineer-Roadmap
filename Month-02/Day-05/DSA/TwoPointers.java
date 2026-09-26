import java.util.*;

/**
 * Two Pointers Pattern in Java
 *
 * Problems Covered:
 *   1. LeetCode 167 - Two Sum II (Input Array Is Sorted) -> O(N) time, O(1) space
 *   2. LeetCode 15 - 3Sum -> O(N^2) time, O(1) extra space
 *   3. LeetCode 11 - Container With Most Water -> O(N) time, O(1) space
 */
public class TwoPointers {

    /**
     * LC 167: Two Sum II - Input array is sorted (1-based index)
     */
    public int[] twoSumSorted(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) {
                return new int[]{left + 1, right + 1};
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
        return new int[]{-1, -1};
    }

    /**
     * LC 15: 3Sum - Unique triplets summing to zero
     */
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();
        int n = nums.length;

        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return result;
    }

    /**
     * LC 11: Container With Most Water
     */
    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int maxWater = 0;

        while (left < right) {
            int h = Math.min(height[left], height[right]);
            int width = right - left;
            maxWater = Math.max(maxWater, h * width);

            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxWater;
    }

    public static void main(String[] args) {
        TwoPointers tp = new TwoPointers();

        // 1. Two Sum II
        int[] res1 = tp.twoSumSorted(new int[]{2, 7, 11, 15}, 9);
        System.out.println("Two Sum II: [" + res1[0] + ", " + res1[1] + "]"); // [1, 2]

        // 2. 3Sum
        List<List<Integer>> res2 = tp.threeSum(new int[]{-1, 0, 1, 2, -1, -4});
        System.out.println("3Sum: " + res2); // [[-1, -1, 2], [-1, 0, 1]]

        // 3. Container With Most Water
        int res3 = tp.maxArea(new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7});
        System.out.println("Max Water Area: " + res3); // 49
    }
}
