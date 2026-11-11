package Month08.Day04;

import java.util.HashMap;
import java.util.Map;

/**
 * Timed Set: Sliding Window
 * LC 3: Longest Substring Without Repeating Characters - O(N) time with two pointers.
 */
public class SlidingWindowTimedSet {

    public static int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> lastSeen = new HashMap<>();
        int maxLength = 0, left = 0;

        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (lastSeen.containsKey(ch)) {
                left = Math.max(left, lastSeen.get(ch) + 1);
            }
            lastSeen.put(ch, right);
            maxLength = Math.max(maxLength, right - left + 1);
        }
        return maxLength;
    }

    public static void main(String[] args) {
        assert lengthOfLongestSubstring("abcabcbb") == 3;
        assert lengthOfLongestSubstring("bbbbb") == 1;
        assert lengthOfLongestSubstring("pwwkew") == 3;

        System.out.println("Day 04 Sliding Window Timed Set verification passed.");
    }
}
