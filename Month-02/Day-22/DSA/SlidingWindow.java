/**
 * Day 22 DSA — Sliding Window Patterns
 *
 * Problems:
 *   1. LC 3   - Longest Substring Without Repeating Characters
 *   2. LC 209 - Minimum Size Subarray Sum
 *   3. LC 438 - Find All Anagrams in a String
 *
 * Pattern: Expand right pointer, shrink left when constraint violated.
 * Time: O(n) | Space: O(k) where k = charset/window size
 */
import java.util.*;

public class SlidingWindow {

    // LC 3 - Longest Substring Without Repeating Characters
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int max = 0, l = 0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            if (map.containsKey(c)) l = Math.max(l, map.get(c) + 1);
            map.put(c, r);
            max = Math.max(max, r - l + 1);
        }
        return max;
    }

    // LC 209 - Minimum Size Subarray Sum
    public int minSubArrayLen(int target, int[] nums) {
        int l = 0, sum = 0, min = Integer.MAX_VALUE;
        for (int r = 0; r < nums.length; r++) {
            sum += nums[r];
            while (sum >= target) {
                min = Math.min(min, r - l + 1);
                sum -= nums[l++];
            }
        }
        return min == Integer.MAX_VALUE ? 0 : min;
    }

    // LC 438 - Find All Anagrams in a String
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        if (s.length() < p.length()) return res;
        int[] pCount = new int[26], wCount = new int[26];
        for (char c : p.toCharArray()) pCount[c - 'a']++;
        for (int r = 0; r < s.length(); r++) {
            wCount[s.charAt(r) - 'a']++;
            if (r >= p.length()) wCount[s.charAt(r - p.length()) - 'a']--;
            if (Arrays.equals(pCount, wCount)) res.add(r - p.length() + 1);
        }
        return res;
    }

    public static void main(String[] args) {
        SlidingWindow sol = new SlidingWindow();

        System.out.println(sol.lengthOfLongestSubstring("abcabcbb")); // 3
        System.out.println(sol.lengthOfLongestSubstring("pwwkew"));   // 3
        System.out.println(sol.minSubArrayLen(7, new int[]{2,3,1,2,4,3})); // 2
        System.out.println(sol.findAnagrams("cbaebabacd", "abc"));    // [0, 6]
    }
}
