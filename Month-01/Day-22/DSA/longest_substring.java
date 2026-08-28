import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Problem: Longest Substring Without Repeating Characters (LeetCode 3)
 * 
 * Given a string s, find the length of the longest substring without repeating characters.
 * 
 * Approaches:
 * 1. Sliding Window with HashSet (Standard):
 *    - Maintain a window [left, right] using a HashSet to store unique characters.
 *    - If s[right] is already in the set, remove s[left] and increment left until s[right] can be added.
 *    - Time Complexity: O(2 * N) = O(N) because each character is visited at most twice.
 *    - Space Complexity: O(min(N, M)) where M is the character set size (e.g. 128 for ASCII).
 * 
 * 2. Optimized Sliding Window with HashMap (Index Map):
 *    - Instead of incrementally moving left, directly jump left to `lastSeenIndex + 1`.
 *    - `left = Math.max(left, map.get(c) + 1)` ensures left never moves backward.
 *    - Time Complexity: O(N) (single pass)
 *    - Space Complexity: O(min(N, M))
 * 
 * 3. Array-based Direct Mapping (for ASCII):
 *    - Use an int[128] array initialized to -1 to store the last seen index of each character.
 *    - Time Complexity: O(N) with lowest constant factor.
 *    - Space Complexity: O(1) fixed 128 integers.
 */
public class longest_substring {

    // =========================================================================
    // Approach 1: Sliding Window with HashSet
    // =========================================================================
    public static int lengthOfLongestSubstringSet(String s) {
        if (s == null || s.isEmpty()) return 0;

        Set<Character> charSet = new HashSet<>();
        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char curr = s.charAt(right);
            // Shrink window from the left until duplicate is removed
            while (charSet.contains(curr)) {
                charSet.remove(s.charAt(left));
                left++;
            }
            charSet.add(curr);
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    // =========================================================================
    // Approach 2: Optimized Sliding Window with HashMap (Jump index)
    // =========================================================================
    public static int lengthOfLongestSubstringMap(String s) {
        if (s == null || s.isEmpty()) return 0;

        Map<Character, Integer> lastSeen = new HashMap<>();
        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char curr = s.charAt(right);

            if (lastSeen.containsKey(curr)) {
                // Advance left pointer past previous occurrence if within current window
                left = Math.max(left, lastSeen.get(curr) + 1);
            }

            lastSeen.put(curr, right);
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    // =========================================================================
    // Approach 3: Optimized Direct ASCII Array Mapping
    // =========================================================================
    public static int lengthOfLongestSubstringArray(String s) {
        if (s == null || s.isEmpty()) return 0;

        int[] lastPos = new int[128];
        for (int i = 0; i < 128; i++) {
            lastPos[i] = -1;
        }

        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char curr = s.charAt(right);
            if (curr < 128 && lastPos[curr] != -1) {
                left = Math.max(left, lastPos[curr] + 1);
            }
            if (curr < 128) {
                lastPos[curr] = right;
            }
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    // =========================================================================
    // Helper to extract actual longest unique substring (for demonstration)
    // =========================================================================
    public static String getLongestUniqueSubstring(String s) {
        if (s == null || s.isEmpty()) return "";

        int[] lastPos = new int[128];
        for (int i = 0; i < 128; i++) lastPos[i] = -1;

        int maxLength = 0;
        int bestStart = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char curr = s.charAt(right);
            if (curr < 128 && lastPos[curr] != -1) {
                left = Math.max(left, lastPos[curr] + 1);
            }
            if (curr < 128) {
                lastPos[curr] = right;
            }

            int currLen = right - left + 1;
            if (currLen > maxLength) {
                maxLength = currLen;
                bestStart = left;
            }
        }

        return s.substring(bestStart, bestStart + maxLength);
    }

    // =========================================================================
    // Test Suite & Main Runner
    // =========================================================================
    public static void main(String[] args) {
        System.out.println("===============================================================");
        System.out.println("  LeetCode 3: Longest Substring Without Repeating Characters  ");
        System.out.println("===============================================================\n");

        testCase("abcabcbb", 3, "abc");
        testCase("bbbbb", 1, "b");
        testCase("pwwkew", 3, "wke");
        testCase("", 0, "");
        testCase(" ", 1, " ");
        testCase("au", 2, "au");
        testCase("dvdf", 3, "vdf");
        testCase("tmmzuxt", 5, "mzuxt");
        testCase("abcdefghijklmnopqrstuvwxyz", 26, "abcdefghijklmnopqrstuvwxyz");

        System.out.println("\nAll test cases passed successfully!");
    }

    private static void testCase(String input, int expectedLength, String sampleMatch) {
        int resSet = lengthOfLongestSubstringSet(input);
        int resMap = lengthOfLongestSubstringMap(input);
        int resArr = lengthOfLongestSubstringArray(input);
        String actualSubstring = getLongestUniqueSubstring(input);

        boolean passed = (resSet == expectedLength) && (resMap == expectedLength) && (resArr == expectedLength);

        System.out.printf("Input: \"%s\"%n", input);
        System.out.printf("  Expected Length : %d%n", expectedLength);
        System.out.printf("  Set Approach    : %d%n", resSet);
        System.out.printf("  Map Approach    : %d%n", resMap);
        System.out.printf("  Array Approach  : %d%n", resArr);
        System.out.printf("  Extracted String: \"%s\"%n", actualSubstring);
        System.out.printf("  Status          : %s%n%n", (passed ? "PASSED" : "FAILED"));

        if (!passed) {
            throw new AssertionError("Mismatch in test case for input: " + input);
        }
    }
}
