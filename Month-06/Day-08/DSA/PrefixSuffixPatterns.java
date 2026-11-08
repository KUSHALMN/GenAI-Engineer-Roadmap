/**
 * Prefix and Suffix Patterns Revision
 * Solves core FAANG interview problems:
 * 1. Product of Array Except Self (LC 238) in O(N) time and O(1) extra space
 * 2. Subarray Sum Equals K (LC 560) using Prefix Sum + HashMap
 * 3. Continuous Subarray Sum (LC 523) using Prefix Sum Modulo
 */

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class PrefixSuffixPatterns {

    // 1. LC 238: Product of Array Except Self
    public static int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];

        // Prefix product pass
        result[0] = 1;
        for (int i = 1; i < n; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }

        // Suffix product pass in-place
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] = result[i] * suffix;
            suffix *= nums[i];
        }

        return result;
    }

    // 2. LC 560: Subarray Sum Equals K
    public static int subarraySum(int[] nums, int k) {
        int count = 0;
        int prefixSum = 0;
        Map<Integer, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0, 1); // Base case for prefix equals k directly

        for (int num : nums) {
            prefixSum += num;
            if (prefixMap.containsKey(prefixSum - k)) {
                count += prefixMap.get(prefixSum - k);
            }
            prefixMap.put(prefixSum, prefixMap.getOrDefault(prefixSum, 0) + 1);
        }

        return count;
    }

    // 3. LC 523: Continuous Subarray Sum (multiple of k, length >= 2)
    public static boolean checkSubarraySum(int[] nums, int k) {
        if (nums == null || nums.length < 2) return false;
        Map<Integer, Integer> modMap = new HashMap<>();
        modMap.put(0, -1); // Remainder 0 at index -1
        int prefixSum = 0;

        for (int i = 0; i < nums.length; i++) {
            prefixSum += nums[i];
            int remainder = k == 0 ? prefixSum : prefixSum % k;
            if (remainder < 0) remainder += k;

            if (modMap.containsKey(remainder)) {
                if (i - modMap.get(remainder) >= 2) {
                    return true;
                }
            } else {
                modMap.put(remainder, i);
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println("=== Prefix & Suffix Patterns Verification ===");

        // Test LC 238
        int[] nums1 = {1, 2, 3, 4};
        int[] prod1 = productExceptSelf(nums1);
        System.out.println("LC 238: " + Arrays.toString(prod1) + " (Expected [24, 12, 8, 6])");
        assert prod1[0] == 24 && prod1[3] == 6 : "LC 238 failed";

        // Test LC 560
        int[] nums2 = {1, 1, 1};
        int count2 = subarraySum(nums2, 2);
        System.out.println("LC 560 (k=2): " + count2 + " (Expected 2)");
        assert count2 == 2 : "LC 560 failed";

        // Test LC 523
        int[] nums3 = {23, 2, 4, 6, 7};
        boolean hasSub3 = checkSubarraySum(nums3, 6);
        System.out.println("LC 523 (k=6): " + hasSub3 + " (Expected true)");
        assert hasSub3 : "LC 523 failed";

        System.out.println("All Prefix/Suffix tests passed successfully!");
    }
}
