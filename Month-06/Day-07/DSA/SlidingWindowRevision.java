/**
 * Sliding Window Revision Patterns
 * Solves core FAANG interview sliding window problems:
 * 1. Longest Substring Without Repeating Characters (LC 3)
 * 2. Minimum Window Substring (LC 76)
 * 3. Max Consecutive Ones III (LC 1004) with at most K flips
 */

import java.util.HashMap;
import java.util.Map;

public class SlidingWindowRevision {

    // 1. LC 3: Longest Substring Without Repeating Characters
    public static int lengthOfLongestSubstring(String s) {
        if (s == null || s.length() == 0) return 0;
        int maxLen = 0;
        int left = 0;
        Map<Character, Integer> lastSeen = new HashMap<>();

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (lastSeen.containsKey(c)) {
                left = Math.max(left, lastSeen.get(c) + 1);
            }
            lastSeen.put(c, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }

    // 2. LC 76: Minimum Window Substring
    public static String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) return "";

        Map<Character, Integer> targetCount = new HashMap<>();
        for (char c : t.toCharArray()) {
            targetCount.put(c, targetCount.getOrDefault(c, 0) + 1);
        }

        Map<Character, Integer> windowCount = new HashMap<>();
        int required = targetCount.size();
        int formed = 0;

        int left = 0, right = 0;
        int minLen = Integer.MAX_VALUE;
        int startIdx = 0;

        while (right < s.length()) {
            char c = s.charAt(right);
            windowCount.put(c, windowCount.getOrDefault(c, 0) + 1);

            if (targetCount.containsKey(c) && windowCount.get(c).intValue() == targetCount.get(c).intValue()) {
                formed++;
            }

            // Shrink window from left
            while (left <= right && formed == required) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    startIdx = left;
                }

                char leftChar = s.charAt(left);
                windowCount.put(leftChar, windowCount.get(leftChar) - 1);
                if (targetCount.containsKey(leftChar) && windowCount.get(leftChar) < targetCount.get(leftChar)) {
                    formed--;
                }
                left++;
            }
            right++;
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(startIdx, startIdx + minLen);
    }

    // 3. LC 1004: Max Consecutive Ones III (at most K zeros)
    public static int longestOnes(int[] nums, int k) {
        int left = 0, right = 0;
        int zeroCount = 0;
        int maxLen = 0;

        while (right < nums.length) {
            if (nums[right] == 0) zeroCount++;

            while (zeroCount > k) {
                if (nums[left] == 0) zeroCount--;
                left++;
            }

            maxLen = Math.max(maxLen, right - left + 1);
            right++;
        }
        return maxLen;
    }

    public static void main(String[] args) {
        System.out.println("=== Sliding Window Patterns Verification ===");

        // Test LC 3
        String s1 = "abcabcbb";
        int len1 = lengthOfLongestSubstring(s1);
        System.out.println("LC 3 ('abcabcbb'): " + len1 + " (Expected 3)");
        assert len1 == 3 : "LC 3 failed";

        // Test LC 76
        String s2 = "ADOBECODEBANC", t2 = "ABC";
        String win2 = minWindow(s2, t2);
        System.out.println("LC 76 ('ADOBECODEBANC', 'ABC'): '" + win2 + "' (Expected 'BANC')");
        assert "BANC".equals(win2) : "LC 76 failed";

        // Test LC 1004
        int[] nums3 = {1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0};
        int ones = longestOnes(nums3, 2);
        System.out.println("LC 1004 (k=2): " + ones + " (Expected 6)");
        assert ones == 6 : "LC 1004 failed";

        System.out.println("All Sliding Window tests passed successfully!");
    }
}
