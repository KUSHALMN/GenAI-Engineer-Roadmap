import java.util.*;

/**
 * Day 17: Partition DP — Matrix Chain Multiplication
 * Problem: Given an array p[] which represents the dimensions of matrices such that
 * matrix A[i] has dimensions p[i-1] x p[i], find the minimum operations to multiply the chain.
 *
 * Algorithm:
 * - dp[i][j] = min operations to multiply matrices from i to j.
 * - dp[i][j] = min_{k} (dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j])
 *
 * Time Complexity: O(n^3)
 * Space Complexity: O(n^2)
 */
public class MatrixChainMultiplication {

    public int matrixChainOrder(int[] p) {
        int n = p.length - 1; // Number of matrices
        int[][] dp = new int[n + 1][n + 1];

        // len is the chain length
        for (int len = 2; len <= n; len++) {
            for (int i = 1; i <= n - len + 1; i++) {
                int j = i + len - 1;
                dp[i][j] = Integer.MAX_VALUE;
                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }
        return dp[1][n];
    }

    public static void main(String[] args) {
        MatrixChainMultiplication solver = new MatrixChainMultiplication();
        int[] arr = {1, 2, 3, 4, 3}; // Matrices: 1x2, 2x3, 3x4, 4x3
        int minOps = solver.matrixChainOrder(arr);

        System.out.println("Minimum multiplications for chain: " + minOps);
        assert minOps == 30 : "Expected 30 multiplications";
        System.out.println("Day 17 DSA MatrixChainMultiplication verification passed!");
    }
}
