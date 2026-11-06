import java.util.*;

/**
 * Day 27: String Matching — Knuth-Morris-Pratt (KMP) Algorithm
 * Problem: Find all occurrences of pattern in text in linear time.
 *
 * Algorithm:
 * 1. Precompute Longest Proper Prefix which is also Suffix (LPS) array for pattern in O(M).
 * 2. Match text with pattern; on mismatch, shift pattern using LPS table without re-checking matched characters.
 *
 * Time Complexity: O(N + M)
 * Space Complexity: O(M) for LPS table.
 */
public class KMPAlgorithm {

    private int[] computeLPS(String pattern) {
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

    public List<Integer> search(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        if (m == 0 || m > n) return matches;

        int[] lps = computeLPS(pattern);
        int i = 0, j = 0; // i for text, j for pattern

        while (i < n) {
            if (pattern.charAt(j) == text.charAt(i)) {
                i++;
                j++;
            }
            if (j == m) {
                matches.add(i - j);
                j = lps[j - 1];
            } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return matches;
    }

    public static void main(String[] args) {
        KMPAlgorithm solver = new KMPAlgorithm();
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";
        List<Integer> matches = solver.search(text, pattern);

        System.out.println("KMP match index: " + matches);
        assert matches.contains(10);
        System.out.println("Day 27 DSA KMPAlgorithm verification passed!");
    }
}
