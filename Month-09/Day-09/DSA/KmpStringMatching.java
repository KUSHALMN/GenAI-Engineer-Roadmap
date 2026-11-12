package Month_09.Day_09.DSA;

/**
 * Day 09: Timed DSA Problem Set — Knuth-Morris-Pratt (KMP) String Matching.
 * Focus: LeetCode 28 (Find Index of First Occurrence in a String) - O(N + M) Time, O(M) Space.
 */
public class KmpStringMatching {

    public static int strStr(String haystack, String needle) {
        if (needle.isEmpty()) return 0;
        if (haystack.length() < needle.length()) return -1;

        int[] lps = buildLPS(needle);
        int i = 0; // index for haystack
        int j = 0; // index for needle

        while (i < haystack.length()) {
            if (haystack.charAt(i) == needle.charAt(j)) {
                i++;
                j++;
            }
            if (j == needle.length()) {
                return i - j; // Match found
            } else if (i < haystack.length() && haystack.charAt(i) != needle.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1]; // Fallback using precomputed LPS
                } else {
                    i++;
                }
            }
        }
        return -1;
    }

    private static int[] buildLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int len = 0;
        int i = 1;

        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    public static void main(String[] args) {
        assert strStr("sadbutsad", "sad") == 0 : "Test 1 Failed";
        assert strStr("leetcode", "leeto") == -1 : "Test 2 Failed";
        assert strStr("aabaaabaaac", "aabaaac") == 4 : "Test 3 Failed";

        System.out.println("Day 09 KMP String Matching verification passed.");
    }
}
