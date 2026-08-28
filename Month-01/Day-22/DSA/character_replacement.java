/**
 * Problem: Longest Repeating Character Replacement (LeetCode 424)
 * 
 * You are given a string s and an integer k. You can choose any character of the string
 * and change it to any other uppercase English character. You can perform this operation at most k times.
 * 
 * Return the length of the longest substring containing the same letter you can get after performing the above operations.
 * 
 * Invariant & Mathematical Insight:
 * - In any valid window [left, right], the window length is (right - left + 1).
 * - If the most frequent character occurs `maxCount` times in the window, then the number of characters
 *   we need to replace is `(window_length - maxCount)`.
 * - The window is VALID if: `(window_length - maxCount) <= k`.
 * - If `(window_length - maxCount) > k`, the window is INVALID, and we must shrink by incrementing `left`.
 * 
 * Approaches:
 * 1. Standard Shrinking Sliding Window:
 *    - Maintain character frequencies in an array `count[26]`.
 *    - Expand `right` and update `maxCount = Math.max(maxCount, count[char])`.
 *    - When `(right - left + 1) - maxCount > k`, decrement `count[s.charAt(left)]` and `left++`.
 *    - Time Complexity: O(N)
 *    - Space Complexity: O(1) (fixed 26 letters).
 * 
 * 2. Non-Shrinking Sliding Window (Optimized):
 *    - Instead of shrinking the window with a while loop, we only slide it (shift left by 1 if invalid).
 *    - The window size never decreases; it only grows when a larger valid window is discovered.
 *    - At the end, the total window length `right - left` is the maximum valid size.
 *    - Time Complexity: O(N)
 *    - Space Complexity: O(1)
 */
public class character_replacement {

    // =========================================================================
    // Approach 1: Standard Sliding Window (with while loop shrink)
    // =========================================================================
    public static int characterReplacementStandard(String s, int k) {
        if (s == null || s.isEmpty()) return 0;

        int[] count = new int[26];
        int maxFreq = 0;
        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char curr = s.charAt(right);
            count[curr - 'A']++;
            maxFreq = Math.max(maxFreq, count[curr - 'A']);

            // Window is invalid if characters to replace > k
            while ((right - left + 1) - maxFreq > k) {
                count[s.charAt(left) - 'A']--;
                left++;
                // Note: maxFreq doesn't need to be strictly decremented because
                // maxLength only expands when a strictly greater maxFreq is found.
            }

            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    // =========================================================================
    // Approach 2: Non-Shrinking Sliding Window (Fastest / Idiomatic)
    // =========================================================================
    public static int characterReplacementOptimized(String s, int k) {
        if (s == null || s.isEmpty()) return 0;

        int[] count = new int[26];
        int maxFreq = 0;
        int left = 0;
        int right = 0;

        for (; right < s.length(); right++) {
            count[s.charAt(right) - 'A']++;
            maxFreq = Math.max(maxFreq, count[s.charAt(right) - 'A']);

            // If invalid, shift the entire window forward by 1 without shrinking
            if ((right - left + 1) - maxFreq > k) {
                count[s.charAt(left) - 'A']--;
                left++;
            }
        }

        return right - left;
    }

    // =========================================================================
    // Test Suite & Main Runner
    // =========================================================================
    public static void main(String[] args) {
        System.out.println("===============================================================");
        System.out.println("  LeetCode 424: Longest Repeating Character Replacement       ");
        System.out.println("===============================================================\n");

        testCase("ABAB", 2, 4);
        testCase("AABABBA", 1, 4);
        testCase("AAAA", 2, 4);
        testCase("ABCDE", 1, 2);
        testCase("ABCDE", 0, 1);
        testCase("BAAA", 0, 3);
        testCase("ABBB", 2, 4);
        testCase("KUSHAL", 2, 3);
        testCase("AABABBA", 2, 5);

        System.out.println("\nAll test cases passed successfully!");
    }

    private static void testCase(String s, int k, int expected) {
        int resStd = characterReplacementStandard(s, k);
        int resOpt = characterReplacementOptimized(s, k);

        boolean passed = (resStd == expected) && (resOpt == expected);

        System.out.printf("Input: s = \"%s\", k = %d%n", s, k);
        System.out.printf("  Expected Length  : %d%n", expected);
        System.out.printf("  Standard Sliding : %d%n", resStd);
        System.out.printf("  Optimized Window : %d%n", resOpt);
        System.out.printf("  Status           : %s%n%n", (passed ? "PASSED" : "FAILED"));

        if (!passed) {
            throw new AssertionError(String.format("Mismatch for s=\"%s\", k=%d. Expected %d, got std=%d, opt=%d",
                    s, k, expected, resStd, resOpt));
        }
    }
}
