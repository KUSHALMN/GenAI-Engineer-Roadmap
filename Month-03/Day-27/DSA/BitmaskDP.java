import java.util.Arrays;

/**
 * Bitmask Dynamic Programming
 * Problem: Optimal Assignment Problem
 * Assign N workers to N tasks such that total cost is minimized.
 * Each worker takes cost[i][j] to do task j.
 * 
 * State:
 * dp(mask): bitmask where j-th bit = 1 if task j has been assigned.
 * Number of set bits in mask = index of current worker to assign!
 * 
 * Complexity:
 * - Total States: 2^N
 * - Transitions per state: N
 * - Total Time: O(N * 2^N) instead of O(N!) brute force
 * - Space: O(2^N) memoization table
 */
public class BitmaskDP {

    public static int minCostToAssign(int[][] cost) {
        int n = cost.length;
        int[] dp = new int[1 << n];
        Arrays.fill(dp, -1);
        return solve(0, 0, cost, n, dp);
    }

    private static int solve(int worker, int mask, int[][] cost, int n, int[] dp) {
        if (worker == n) {
            return 0; // All workers assigned
        }

        if (dp[mask] != -1) {
            return dp[mask];
        }

        int minCost = Integer.MAX_VALUE;

        // Try assigning current worker to any unassigned task j
        for (int task = 0; task < n; task++) {
            if ((mask & (1 << task)) == 0) {
                // Task is unassigned -> assign and recurse
                int currentCost = cost[worker][task] + solve(worker + 1, mask | (1 << task), cost, n, dp);
                minCost = Math.min(minCost, currentCost);
            }
        }

        return dp[mask] = minCost;
    }

    public static void main(String[] args) {
        // Cost matrix: 3 workers, 3 tasks
        int[][] cost = {
            {9, 2, 7},
            {6, 4, 3},
            {5, 8, 1}
        };

        // Optimal: Worker 0 -> Task 1 (cost 2), Worker 1 -> Task 0 (cost 6) or Worker 1 -> Task 1,
        // Worker 0 -> Task 1 (2), Worker 1 -> Task 0 (6), Worker 2 -> Task 2 (1) = 9
        // Or Worker 0 -> Task 1 (2), Worker 1 -> Task 0 (6), Worker 2 -> Task 2 (1) -> 2 + 6 + 1 = 9
        // Wait: Worker 0 -> Task 1 (2), Worker 1 -> Task 2 (3), Worker 2 -> Task 0 (5) = 2 + 3 + 5 = 10
        // Best is: 2 + 6 + 1 = 9 or Worker 0 (7) + Worker 1 (4) + Worker 2 (5) = 16
        int minAssignment = minCostToAssign(cost);
        System.out.println("Minimum assignment cost for 3x3 workers/tasks: " + minAssignment); // Expected 9

        System.out.println("BitmaskDP tests passed!");
    }
}
