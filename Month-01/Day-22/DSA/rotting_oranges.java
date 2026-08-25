import java.util.LinkedList;
import java.util.Queue;

/**
 * Problem: Rotting Oranges (LeetCode 994)
 * 
 * You are given an m x n grid where each cell can have one of three values:
 * - 0 representing an empty cell,
 * - 1 representing a fresh orange, or
 * - 2 representing a rotten orange.
 * 
 * Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
 * Return the minimum number of minutes that must elapse until no cell has a fresh orange. 
 * If this is impossible, return -1.
 * 
 * Core Concept: Multi-Source Breadth-First Search (BFS)
 * - Multi-source BFS expands from ALL rotten oranges simultaneously level by level.
 * - Queue all initial '2's and count initial '1's.
 * - Process queue level-by-level (each level = 1 minute).
 * - Time Complexity: O(M * N)
 * - Space Complexity: O(M * N) queue capacity.
 */
public class rotting_oranges {

    public static int orangesRotting(int[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }

        int rows = grid.length;
        int cols = grid[0].length;
        Queue<int[]> queue = new LinkedList<>();
        int freshCount = 0;

        // 1. Enqueue all initial rotten oranges (multi-sources) and count fresh oranges
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) {
                    queue.offer(new int[]{r, c});
                } else if (grid[r][c] == 1) {
                    freshCount++;
                }
            }
        }

        // If no fresh oranges exist from the start
        if (freshCount == 0) {
            return 0;
        }

        int minutes = 0;
        int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

        // 2. Multi-source BFS level-by-level
        while (!queue.isEmpty() && freshCount > 0) {
            int levelSize = queue.size();
            minutes++;

            for (int i = 0; i < levelSize; i++) {
                int[] curr = queue.poll();
                int currR = curr[0];
                int currC = curr[1];

                for (int[] dir : directions) {
                    int nextR = currR + dir[0];
                    int nextC = currC + dir[1];

                    if (nextR >= 0 && nextR < rows && nextC >= 0 && nextC < cols && grid[nextR][nextC] == 1) {
                        grid[nextR][nextC] = 2; // Rot the fresh orange
                        freshCount--;
                        queue.offer(new int[]{nextR, nextC});
                    }
                }
            }
        }

        return freshCount == 0 ? minutes : -1;
    }

    // Helper: Clone grid for testing
    private static int[][] cloneGrid(int[][] grid) {
        int[][] copy = new int[grid.length][grid[0].length];
        for (int i = 0; i < grid.length; i++) {
            System.arraycopy(grid[i], 0, copy[i], 0, grid[0].length);
        }
        return copy;
    }

    // ==========================================
    // Verification & Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     LeetCode 994: Rotting Oranges Test Suite    ");
        System.out.println("=================================================\n");

        // Test 1: Standard case (4 minutes)
        int[][] grid1 = {
            {2, 1, 1},
            {1, 1, 0},
            {0, 1, 1}
        };
        runTest("Test 1: Standard Rotting (4 mins)", grid1, 4);

        // Test 2: Unreachable fresh orange (-1)
        int[][] grid2 = {
            {2, 1, 1},
            {0, 1, 1},
            {1, 0, 1}
        };
        runTest("Test 2: Unreachable Orange (-1)", grid2, -1);

        // Test 3: No fresh oranges (0 minutes)
        int[][] grid3 = {
            {0, 2}
        };
        runTest("Test 3: No Fresh Oranges (0 mins)", grid3, 0);

        // Test 4: Multiple simultaneous rotten sources
        int[][] grid4 = {
            {2, 1, 1, 2},
            {1, 1, 1, 1}
        };
        runTest("Test 4: Dual Source Parallel Rotting (2 mins)", grid4, 2);

        System.out.println("\nAll Rotting Oranges test cases passed successfully!");
    }

    private static void runTest(String label, int[][] grid, int expected) {
        int[][] copy = cloneGrid(grid);
        int result = orangesRotting(copy);
        boolean ok = (result == expected);
        System.out.printf("[%s] Expected: %d | Result: %d => %s%n",
                label, expected, result, (ok ? "PASSED" : "FAILED"));

        if (!ok) {
            throw new AssertionError("Test failed for: " + label);
        }
    }
}
