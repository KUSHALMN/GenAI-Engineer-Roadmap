import java.util.*;

/**
 * Day 15: Dynamic Programming — Edit Distance (Levenshtein Distance)
 * Problem: Given two strings word1 and word2, return the minimum operations (insert, delete, replace)
 * required to convert word1 to word2.
 *
 * Algorithm:
 * - dp[i][j] = operations to convert word1[0..i-1] to word2[0..j-1]
 * - If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]
 * - Else: 1 + min(replace: dp[i-1][j-1], delete: dp[i-1][j], insert: dp[i][j-1])
 *
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 */
public class EditDistance {

    public int minDistance(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 0; i <= m; i++) dp[i][0] = i; // Deleting all chars
        for (int j = 0; j <= n; j++) dp[0][j] = j; // Inserting all chars

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], // Replace
                                    Math.min(dp[i - 1][j],     // Delete
                                             dp[i][j - 1]));   // Insert
                }
            }
        }
        return dp[m][n];
    }

    public static void main(String[] args) {
        EditDistance solver = new EditDistance();
        int dist = solver.minDistance("horse", "ros");

        System.out.println("Edit distance between 'horse' and 'ros': " + dist);
        assert dist == 3 : "Expected 3 operations (horse -> rorse -> rose -> ros)";
        System.out.println("Day 15 DSA EditDistance verification passed!");
    }
}
