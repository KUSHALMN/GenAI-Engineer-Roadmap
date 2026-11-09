public class DynamicProgramming2DRevision {
    // 1. LC 62: Unique Paths
    public static int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        java.util.Arrays.fill(dp, 1);
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[j] += dp[j - 1];
            }
        }
        return dp[n - 1];
    }

    // 2. LC 1143: Longest Common Subsequence
    public static int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
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
        System.out.println("=== 2D Dynamic Programming Verification ===");
        int paths = uniquePaths(3, 7);
        System.out.println("LC 62 (Unique Paths 3x7): " + paths + " (Expected 28)");
        assert paths == 28 : "LC 62 failed";

        int lcs = longestCommonSubsequence("abcde", "ace");
        System.out.println("LC 1143 (LCS 'abcde', 'ace'): " + lcs + " (Expected 3)");
        assert lcs == 3 : "LC 1143 failed";
        System.out.println("2D DP tests passed!");
    }
}
