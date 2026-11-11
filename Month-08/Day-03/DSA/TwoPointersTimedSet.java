package Month08.Day03;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Timed Set: Two Pointers
 * LC 15: 3Sum - O(N^2) time with sorted array two pointers and deduplication.
 */
public class TwoPointersTimedSet {

    public static List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();

        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // Skip duplicate anchor
            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    res.add(List.of(nums[i], nums[left], nums[right]));
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
        return res;
    }

    public static void main(String[] args) {
        int[] nums = {-1, 0, 1, 2, -1, -4};
        List<List<Integer>> triplets = threeSum(nums);
        assert triplets.size() == 2;

        System.out.println("Day 03 Two Pointers Timed Set verification passed: " + triplets.size() + " triplets.");
    }
}
