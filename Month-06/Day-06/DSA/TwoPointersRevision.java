/**
 * Two Pointers Revision Patterns
 * Solves core FAANG interview problems:
 * 1. 3Sum (LC 15) with strict duplicate skipping
 * 2. Container With Most Water (LC 11) with greedy contraction
 * 3. Trapping Rain Water (LC 42) in O(N) time and O(1) space
 */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class TwoPointersRevision {

    // 1. LC 15: 3Sum
    public static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null || nums.length < 3) return result;
        Arrays.sort(nums);

        for (int i = 0; i < nums.length - 2; i++) {
            if (nums[i] > 0) break; // Triplet sum cannot be 0 if smallest > 0
            if (i > 0 && nums[i] == nums[i - 1]) continue; // Skip duplicate i

            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++; // Skip dup left
                    while (left < right && nums[right] == nums[right - 1]) right--; // Skip dup right
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

    // 2. LC 11: Container With Most Water
    public static int maxArea(int[] height) {
        int maxWater = 0;
        int left = 0, right = height.length - 1;
        while (left < right) {
            int h = Math.min(height[left], height[right]);
            int area = h * (right - left);
            if (area > maxWater) maxWater = area;

            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxWater;
    }

    // 3. LC 42: Trapping Rain Water (O(1) Space Two Pointers)
    public static int trap(int[] height) {
        if (height == null || height.length <= 2) return 0;
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int totalWater = 0;

        while (left < right) {
            if (height[left] <= height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    totalWater += (leftMax - height[left]);
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    totalWater += (rightMax - height[right]);
                }
                right--;
            }
        }
        return totalWater;
    }

    public static void main(String[] args) {
        System.out.println("=== Two Pointers Patterns Verification ===");

        // Test LC 15
        int[] nums1 = {-1, 0, 1, 2, -1, -4};
        List<List<Integer>> triplets = threeSum(nums1);
        System.out.println("LC 15 (3Sum): " + triplets);
        assert triplets.size() == 2 : "LC 15 failed";

        // Test LC 11
        int[] h1 = {1, 8, 6, 2, 5, 4, 8, 3, 7};
        int water = maxArea(h1);
        System.out.println("LC 11 (Max Water): " + water + " (Expected 49)");
        assert water == 49 : "LC 11 failed";

        // Test LC 42
        int[] h2 = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
        int trapped = trap(h2);
        System.out.println("LC 42 (Trapped Rain Water): " + trapped + " (Expected 6)");
        assert trapped == 6 : "LC 42 failed";

        System.out.println("All Two Pointers tests passed successfully!");
    }
}
