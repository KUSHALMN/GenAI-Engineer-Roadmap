import java.util.HashMap;
import java.util.Map;

/**
 * Sliding Window Pattern in Java
 *
 * Problems Covered:
 *   1. LeetCode 3 - Longest Substring Without Repeating Characters -> O(N) time, O(min(m, n)) space
 *   2. LeetCode 209 - Minimum Size Subarray Sum -> O(N) time, O(1) space
 *   3. LeetCode 643 - Maximum Average Subarray I -> O(N) time, O(1) space
 */
public class SlidingWindow {

    /**
     * LC 3: Longest Substring Without Repeating Characters
     */
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> charMap = new HashMap<>();
        int left = 0;
        int maxLen = 0;

        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (charMap.containsKey(ch) && charMap.get(ch) >= left) {
                left = charMap.get(ch) + 1;
            }
            charMap.put(ch, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }

    /**
     * LC 209: Minimum Size Subarray Sum
     */
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int currentSum = 0;
        int minLen = Integer.MAX_VALUE;

        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];

            while (currentSum >= target) {
                minLen = Math.min(minLen, right - left + 1);
                currentSum -= nums[left];
                left++;
            }
        }
        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }

    /**
     * LC 643: Maximum Average Subarray I (Window size k)
     */
    public double findMaxAverage(int[] nums, int k) {
        long currentSum = 0;
        for (int i = 0; i < k; i++) {
            currentSum += nums[i];
        }

        long maxSum = currentSum;
        for (int i = k; i < nums.length; i++) {
            currentSum += nums[i] - nums[i - k];
            maxSum = Math.max(maxSum, currentSum);
        }

        return (double) maxSum / k;
    }

    public static void main(String[] args) {
        SlidingWindow sw = new SlidingWindow();

        // 1. Longest substring without repeating characters
        int r1 = sw.lengthOfLongestSubstring("abcabcbb");
        System.out.println("LC 3 (abcabcbb): " + r1); // 3

        // 2. Minimum size subarray sum
        int r2 = sw.minSubArrayLen(7, new int[]{2, 3, 1, 2, 4, 3});
        System.out.println("LC 209 (target=7): " + r2); // 2

        // 3. Maximum average subarray
        double r3 = sw.findMaxAverage(new int[]{1, 12, -5, -6, 50, 3}, 4);
        System.out.println("LC 643 (k=4): " + r3); // 12.75
    }
}
