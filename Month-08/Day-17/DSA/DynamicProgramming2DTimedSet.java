package Month_08.Day_17.DSA;

/**
 * Day 17: Timed DSA Problem Set — 2D Dynamic Programming.
 * Focus: LeetCode 1143 (Longest Common Subsequence) & LeetCode 62 (Unique Paths).
 */
public class DynamicProgramming2DTimedSet {

    // LeetCode 1143: Longest Common Subsequence - O(M*N) Time, O(min(M,N)) Space
    public static int longestCommonSubsequence(String text1, String text2) {
        if (text1.length() < text2.length()) {
            return longestCommonSubsequence(text2, text1);
        }
        int m = text1.length();
        int n = text2.length();
        int[] dp = new int[n + 1];

        for (int i = 1; i <= m; i++) {
            int prevDiag = 0;
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[j] = prevDiag + 1;
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]);
                }
                prevDiag = temp;
            }
        }
        return dp[n];
    }

    // LeetCode 62: Unique Paths - O(M*N) Time, O(N) Space
    public static int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        for (int j = 0; j < n; j++) dp[j] = 1;

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[j] += dp[j - 1];
            }
        }
        return dp[n - 1];
    }

    public static void main(String[] args) {
        // LC 1143 tests
        assert longestCommonSubsequence("abcde", "ace") == 3 : "Test 1 Failed";
        assert longestCommonSubsequence("abc", "abc") == 3 : "Test 2 Failed";
        assert longestCommonSubsequence("abc", "def") == 0 : "Test 3 Failed";

        // LC 62 tests
        assert uniquePaths(3, 7) == 28 : "LC 62 Test 1 Failed";
        assert uniquePaths(3, 2) == 3 : "LC 62 Test 2 Failed";

        System.out.println("Day 17 2D Dynamic Programming Timed Set verification passed.");
    }
}
