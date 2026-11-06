import java.util.*;

/**
 * Day 14: Dynamic Programming — Longest Common Subsequence (LCS)
 * Problem: Given two strings text1 and text2, return the length of their longest common subsequence.
 *
 * Algorithm:
 * - 2D DP Table of size (m+1) x (n+1)
 * - If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
 * - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
 *
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n) (or O(min(m, n)) optimized)
 */
public class LongestCommonSubsequence {

    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }

    public static void main(String[] args) {
        LongestCommonSubsequence solver = new LongestCommonSubsequence();
        String text1 = "abcde";
        String text2 = "ace";
        int lcs = solver.longestCommonSubsequence(text1, text2);

        System.out.println("LCS for 'abcde' and 'ace': " + lcs);
        assert lcs == 3 : "Expected 3 ('ace')";
        System.out.println("Day 14 DSA LongestCommonSubsequence verification passed!");
    }
}
