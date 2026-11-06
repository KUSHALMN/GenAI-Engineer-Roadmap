import java.util.*;

/**
 * Day 29: 2D Dynamic Programming — Wildcard Matching
 * Problem: Implement wildcard pattern matching with support for '?' (matches any single character)
 * and '*' (matches any sequence of characters, including empty).
 *
 * Algorithm:
 * - dp[i][j] = boolean whether s[0..i-1] matches p[0..j-1]
 * - If p[j-1] == '?' or s[i-1] == p[j-1]: dp[i][j] = dp[i-1][j-1]
 * - Else if p[j-1] == '*': dp[i][j] = dp[i][j-1] (empty) || dp[i-1][j] (one or more)
 *
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 */
public class WildcardMatching {

    public boolean isMatch(String s, String p) {
        int m = s.length();
        int n = p.length();
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;

        // Initialize for patterns starting with '*'
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 1];
            }
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char sc = s.charAt(i - 1);
                char pc = p.charAt(j - 1);

                if (pc == '?' || sc == pc) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (pc == '*') {
                    dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
                }
            }
        }
        return dp[m][n];
    }

    public static void main(String[] args) {
        WildcardMatching solver = new WildcardMatching();
        assert solver.isMatch("aa", "*") : "Expected true for 'aa' and '*'";
        assert !solver.isMatch("cb", "?a") : "Expected false for 'cb' and '?a'";
        assert solver.isMatch("adceb", "*a*b") : "Expected true for 'adceb' and '*a*b'";

        System.out.println("Day 29 DSA WildcardMatching verification passed!");
    }
}
