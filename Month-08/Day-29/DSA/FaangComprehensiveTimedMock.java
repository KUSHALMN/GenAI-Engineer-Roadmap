package Month_08.Day_29.DSA;

import java.util.HashMap;
import java.util.Map;

/**
 * Day 29: Timed DSA Problem Set — FAANG Comprehensive Mock Set.
 * Focus: LeetCode 4 (Median of Two Sorted Arrays) & LeetCode 76 (Minimum Window Substring).
 */
public class FaangComprehensiveTimedMock {

    // LeetCode 4: Median of Two Sorted Arrays - O(log(min(M, N))) Time, O(1) Space
    public static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }
        int m = nums1.length, n = nums2.length;
        int low = 0, high = m;

        while (low <= high) {
            int partitionX = (low + high) / 2;
            int partitionY = (m + n + 1) / 2 - partitionX;

            int maxLeftX = (partitionX == 0) ? Integer.MIN_VALUE : nums1[partitionX - 1];
            int minRightX = (partitionX == m) ? Integer.MAX_VALUE : nums1[partitionX];

            int maxLeftY = (partitionY == 0) ? Integer.MIN_VALUE : nums2[partitionY - 1];
            int minRightY = (partitionY == n) ? Integer.MAX_VALUE : nums2[partitionY];

            if (maxLeftX <= minRightY && maxLeftY <= minRightX) {
                if ((m + n) % 2 == 0) {
                    return ((double) Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2;
                } else {
                    return (double) Math.max(maxLeftX, maxLeftY);
                }
            } else if (maxLeftX > minRightY) {
                high = partitionX - 1;
            } else {
                low = partitionX + 1;
            }
        }
        throw new IllegalArgumentException("Input arrays not sorted");
    }

    // LeetCode 76: Minimum Window Substring - O(M + N) Time, O(1) Space (Sliding Window)
    public static String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";

        int[] map = new int[128];
        for (char c : t.toCharArray()) {
            map[c]++;
        }

        int count = t.length();
        int left = 0, right = 0;
        int minLen = Integer.MAX_VALUE;
        int startIdx = 0;

        while (right < s.length()) {
            if (map[s.charAt(right++)]-- > 0) {
                count--;
            }
            while (count == 0) {
                if (right - left < minLen) {
                    minLen = right - left;
                    startIdx = left;
                }
                if (map[s.charAt(left++)]++ == 0) {
                    count++;
                }
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(startIdx, startIdx + minLen);
    }

    public static void main(String[] args) {
        // LC 4 tests
        assert findMedianSortedArrays(new int[]{1, 3}, new int[]{2}) == 2.0 : "LC 4 Test 1 Failed";
        assert findMedianSortedArrays(new int[]{1, 2}, new int[]{3, 4}) == 2.5 : "LC 4 Test 2 Failed";

        // LC 76 tests
        assert minWindow("ADOBECODEBANC", "ABC").equals("BANC") : "LC 76 Test 1 Failed";
        assert minWindow("a", "a").equals("a") : "LC 76 Test 2 Failed";
        assert minWindow("a", "aa").equals("") : "LC 76 Test 3 Failed";

        System.out.println("Day 29 FAANG Comprehensive Timed Mock (LC 4 & LC 76) verification passed.");
    }
}
