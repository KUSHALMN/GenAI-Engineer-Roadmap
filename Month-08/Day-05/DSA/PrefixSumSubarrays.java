package Month08.Day05;

import java.util.HashMap;
import java.util.Map;

/**
 * Timed Set: Prefix Sums & Subarrays
 * LC 560: Subarray Sum Equals K - O(N) time with prefix sum frequency map.
 */
public class PrefixSumSubarrays {

    public static int subarraySum(int[] nums, int k) {
        int count = 0, currentSum = 0;
        Map<Integer, Integer> prefixCounts = new HashMap<>();
        prefixCounts.put(0, 1); // Base case for subarrays starting at index 0

        for (int num : nums) {
            currentSum += num;
            if (prefixCounts.containsKey(currentSum - k)) {
                count += prefixCounts.get(currentSum - k);
            }
            prefixCounts.put(currentSum, prefixCounts.getOrDefault(currentSum, 0) + 1);
        }
        return count;
    }

    public static void main(String[] args) {
        int[] nums = {1, 1, 1};
        assert subarraySum(nums, 2) == 2;

        int[] nums2 = {1, 2, 3};
        assert subarraySum(nums2, 3) == 2;

        System.out.println("Day 05 Prefix Sums & Subarrays verification passed.");
    }
}
