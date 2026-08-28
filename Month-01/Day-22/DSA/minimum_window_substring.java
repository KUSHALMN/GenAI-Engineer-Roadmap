import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Problem: Minimum Window Substring (LeetCode 76 - Hard)
 * 
 * Given two strings s and t of lengths m and n respectively, return the minimum window 
 * substring of s such that every character in t (including duplicates) is included in the window. 
 * If there is no such substring, return the empty string "".
 * 
 * Invariants & Concepts:
 * - We need to find the smallest range [left, right] such that the count of every character
 *   c in t is <= count of c in s[left...right].
 * - `needCount`: The number of unique characters in t that must satisfy the required frequency.
 * - `haveCount`: The number of unique characters whose frequency requirement is met in the current window.
 * - When `haveCount == needCount`, the window is valid. We try to shrink from `left` to find the minimal window.
 * 
 * Approaches:
 * 1. Two-Pointer Sliding Window with Frequency Arrays (ASCII direct mapping):
 *    - `targetFreq[128]`: stores required counts from t.
 *    - `windowFreq[128]`: tracks counts in current window.
 *    - Time Complexity: O(M + N) where M = s.length(), N = t.length()
 *    - Space Complexity: O(1) (fixed 128 integer arrays)
 * 
 * 2. Filtered Window with Index Pairs (Optimized for sparse t in very large s):
 *    - Pre-filter s to keep only characters and indices that appear in t.
 *    - Slide over the filtered list to avoid traversing useless characters.
 *    - Time Complexity: O(|filtered_S| + |S| + |T|)
 *    - Space Complexity: O(|S| + |T|)
 */
public class minimum_window_substring {

    // =========================================================================
    // Approach 1: Direct ASCII Frequency Array Sliding Window (Optimal)
    // =========================================================================
    public static String minWindowArray(String s, String t) {
        if (s == null || t == null || s.length() < t.length() || t.isEmpty()) {
            return "";
        }

        int[] targetFreq = new int[128];
        int uniqueCharsToMatch = 0;

        for (int i = 0; i < t.length(); i++) {
            char c = t.charAt(i);
            if (targetFreq[c] == 0) {
                uniqueCharsToMatch++;
            }
            targetFreq[c]++;
        }

        int[] windowFreq = new int[128];
        int matchedChars = 0;

        int minLen = Integer.MAX_VALUE;
        int minStart = 0;

        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char rChar = s.charAt(right);
            windowFreq[rChar]++;

            // If frequency of rChar meets target requirement exactly
            if (targetFreq[rChar] > 0 && windowFreq[rChar] == targetFreq[rChar]) {
                matchedChars++;
            }

            // Once window is valid, contract from left
            while (matchedChars == uniqueCharsToMatch) {
                int currentLen = right - left + 1;
                if (currentLen < minLen) {
                    minLen = currentLen;
                    minStart = left;
                }

                char lChar = s.charAt(left);
                windowFreq[lChar]--;
                if (targetFreq[lChar] > 0 && windowFreq[lChar] < targetFreq[lChar]) {
                    matchedChars--;
                }
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
    }

    // =========================================================================
    // Approach 2: Map-based Sliding Window (Generic Character Support)
    // =========================================================================
    public static String minWindowMap(String s, String t) {
        if (s == null || t == null || s.length() < t.length() || t.isEmpty()) {
            return "";
        }

        Map<Character, Integer> targetMap = new HashMap<>();
        for (char c : t.toCharArray()) {
            targetMap.put(c, targetMap.getOrDefault(c, 0) + 1);
        }

        int required = targetMap.size();
        int formed = 0;

        Map<Character, Integer> windowCounts = new HashMap<>();

        int[] ans = {-1, 0, 0}; // length, left, right
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            windowCounts.put(c, windowCounts.getOrDefault(c, 0) + 1);

            if (targetMap.containsKey(c) && windowCounts.get(c).intValue() == targetMap.get(c).intValue()) {
                formed++;
            }

            while (left <= right && formed == required) {
                c = s.charAt(left);

                // Update minimal answer
                if (ans[0] == -1 || (right - left + 1) < ans[0]) {
                    ans[0] = right - left + 1;
                    ans[1] = left;
                    ans[2] = right;
                }

                windowCounts.put(c, windowCounts.get(c) - 1);
                if (targetMap.containsKey(c) && windowCounts.get(c) < targetMap.get(c)) {
                    formed--;
                }
                left++;
            }
        }

        return ans[0] == -1 ? "" : s.substring(ans[1], ans[2] + 1);
    }

    // =========================================================================
    // Approach 3: Filtered S Sliding Window (Sparse target optimization)
    // =========================================================================
    static class Pair {
        int index;
        char character;
        Pair(int index, char character) {
            this.index = index;
            this.character = character;
        }
    }

    public static String minWindowFiltered(String s, String t) {
        if (s == null || t == null || s.length() < t.length() || t.isEmpty()) {
            return "";
        }

        Map<Character, Integer> targetMap = new HashMap<>();
        for (char c : t.toCharArray()) {
            targetMap.put(c, targetMap.getOrDefault(c, 0) + 1);
        }

        List<Pair> filteredS = new ArrayList<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (targetMap.containsKey(c)) {
                filteredS.add(new Pair(i, c));
            }
        }

        int required = targetMap.size();
        int formed = 0;
        Map<Character, Integer> windowCounts = new HashMap<>();

        int minLen = Integer.MAX_VALUE;
        int minStart = 0;
        int left = 0;

        for (int right = 0; right < filteredS.size(); right++) {
            char c = filteredS.get(right).character;
            windowCounts.put(c, windowCounts.getOrDefault(c, 0) + 1);

            if (windowCounts.get(c).intValue() == targetMap.get(c).intValue()) {
                formed++;
            }

            while (left <= right && formed == required) {
                int start = filteredS.get(left).index;
                int end = filteredS.get(right).index;
                int currentLen = end - start + 1;

                if (currentLen < minLen) {
                    minLen = currentLen;
                    minStart = start;
                }

                char lChar = filteredS.get(left).character;
                windowCounts.put(lChar, windowCounts.get(lChar) - 1);
                if (windowCounts.get(lChar) < targetMap.get(lChar)) {
                    formed--;
                }
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
    }

    // =========================================================================
    // Test Suite & Main Runner
    // =========================================================================
    public static void main(String[] args) {
        System.out.println("===============================================================");
        System.out.println("  LeetCode 76: Minimum Window Substring (Hard) Test Suite      ");
        System.out.println("===============================================================\n");

        testCase("ADOBECODEBANC", "ABC", "BANC");
        testCase("a", "a", "a");
        testCase("a", "aa", "");
        testCase("ab", "b", "b");
        testCase("aaflslflsldkalskaaa", "aaa", "aaa");
        testCase("cabwefgewcwaefgcf", "cae", "cwae");
        testCase("DONOTPANIC", "TOP", "OTP");
        testCase("A", "B", "");

        System.out.println("\nAll test cases passed successfully!");
    }

    private static void testCase(String s, String t, String expected) {
        String resArr = minWindowArray(s, t);
        String resMap = minWindowMap(s, t);
        String resFiltered = minWindowFiltered(s, t);

        boolean passed = resArr.equals(expected) && resMap.equals(expected) && resFiltered.equals(expected);

        System.out.printf("Input: s = \"%s\", t = \"%s\"%n", s, t);
        System.out.printf("  Expected Window : \"%s\"%n", expected);
        System.out.printf("  Array Approach  : \"%s\"%n", resArr);
        System.out.printf("  Map Approach    : \"%s\"%n", resMap);
        System.out.printf("  Filtered Approach: \"%s\"%n", resFiltered);
        System.out.printf("  Status          : %s%n%n", (passed ? "PASSED" : "FAILED"));

        if (!passed) {
            throw new AssertionError(String.format("Mismatch for s=\"%s\", t=\"%s\". Expected \"%s\", got \"%s\"",
                    s, t, expected, resArr));
        }
    }
}
