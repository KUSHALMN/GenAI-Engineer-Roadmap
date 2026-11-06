import java.util.*;

/**
 * Day 10: Dynamic Programming Tabulation — Unique Paths & Minimum Path Sum
 * Problem: Given an m x n grid, find total unique paths from top-left to bottom-right (moving only right or down).
 *
 * Algorithm:
 * - dp[r][c] = dp[r-1][c] + dp[r][c-1]
 * - Space optimization: single row buffer of length n.
 *
 * Time Complexity: O(m * n)
 * Space Complexity: O(n)
 */
public class DPBottomUp {

    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1); // Top row initialized to 1 path

        for (int r = 1; r < m; r++) {
            for (int c = 1; c < n; c++) {
                dp[c] += dp[c - 1]; // current = current (from top) + previous (from left)
            }
        }
        return dp[n - 1];
    }

    public static void main(String[] args) {
        DPBottomUp solver = new DPBottomUp();
        int paths = solver.uniquePaths(3, 7);

        System.out.println("Unique paths for 3x7 grid: " + paths);
        assert paths == 28 : "Expected 28 unique paths for 3x7";
        System.out.println("Day 10 DSA DPBottomUp verification passed!");
    }
}
