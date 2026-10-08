import java.util.*;

/**
 * Day 08 (Month 03) DSA: Graph Grid Traversal & Connected Components
 * - LeetCode 200: Number of Islands (DFS in-place sinking + BFS Queue)
 * - LeetCode 695: Max Area of Island
 * 
 * Invariants:
 * 1. Grid cells with '1' represent unvisited land; mutating to '0' marks them visited without extra memory.
 * 2. 4-directional transitions: {-1, 0}, {1, 0}, {0, -1}, {0, 1}.
 * 3. Each island corresponds to one connected component in the grid graph.
 */
public class NumberOfIslands {

    // -------------------------------------------------------------
    // LC 200: Number of Islands via DFS - O(M * N) Time, O(M * N) Space (Call Stack)
    // -------------------------------------------------------------
    public static int numIslandsDFS(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;

        int m = grid.length;
        int n = grid[0].length;
        int islandCount = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == '1') {
                    islandCount++;
                    dfsSink(grid, r, c, m, n);
                }
            }
        }

        return islandCount;
    }

    private static void dfsSink(char[][] grid, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') {
            return;
        }

        grid[r][c] = '0'; // Sink the land to mark visited

        dfsSink(grid, r - 1, c, m, n); // Up
        dfsSink(grid, r + 1, c, m, n); // Down
        dfsSink(grid, r, c - 1, m, n); // Left
        dfsSink(grid, r, c + 1, m, n); // Right
    }

    // -------------------------------------------------------------
    // LC 200 Alternative: Number of Islands via BFS - O(M * N) Time, O(min(M, N)) Space
    // -------------------------------------------------------------
    public static int numIslandsBFS(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;

        int m = grid.length;
        int n = grid[0].length;
        int islandCount = 0;
        int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == '1') {
                    islandCount++;
                    grid[r][c] = '0';
                    Queue<int[]> queue = new LinkedList<>();
                    queue.offer(new int[]{r, c});

                    while (!queue.isEmpty()) {
                        int[] curr = queue.poll();
                        for (int[] d : DIRS) {
                            int nr = curr[0] + d[0];
                            int nc = curr[1] + d[1];
                            if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == '1') {
                                grid[nr][nc] = '0';
                                queue.offer(new int[]{nr, nc});
                            }
                        }
                    }
                }
            }
        }

        return islandCount;
    }

    // -------------------------------------------------------------
    // LC 695: Max Area of Island - O(M * N) Time, O(M * N) Space
    // -------------------------------------------------------------
    public static int maxAreaOfIsland(int[][] grid) {
        if (grid == null || grid.length == 0) return 0;

        int m = grid.length;
        int n = grid[0].length;
        int maxArea = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) {
                    maxArea = Math.max(maxArea, dfsArea(grid, r, c, m, n));
                }
            }
        }

        return maxArea;
    }

    private static int dfsArea(int[][] grid, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != 1) {
            return 0;
        }

        grid[r][c] = 0;
        return 1 + dfsArea(grid, r - 1, c, m, n)
                 + dfsArea(grid, r + 1, c, m, n)
                 + dfsArea(grid, r, c - 1, m, n)
                 + dfsArea(grid, r, c + 1, m, n);
    }

    // -------------------------------------------------------------
    // Verification & Test Suite
    // -------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  Day 08 DSA: Number of Islands & Max Area Tests ");
        System.out.println("=================================================\n");

        char[][] grid1 = {
            {'1', '1', '1', '1', '0'},
            {'1', '1', '0', '1', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '0', '0', '0'}
        };
        int islands1 = numIslandsDFS(grid1);
        System.out.println("Grid 1 Islands (DFS): " + islands1 + " (Expected: 1)");
        assert islands1 == 1;

        char[][] grid2 = {
            {'1', '1', '0', '0', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '1', '0', '0'},
            {'0', '0', '0', '1', '1'}
        };
        int islands2 = numIslandsBFS(grid2);
        System.out.println("Grid 2 Islands (BFS): " + islands2 + " (Expected: 3)");
        assert islands2 == 3;

        int[][] areaGrid = {
            {0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0},
            {0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0},
            {0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0}
        };
        int maxArea = maxAreaOfIsland(areaGrid);
        System.out.println("Max Area of Island: " + maxArea + " (Expected: 6)");
        assert maxArea == 6;

        System.out.println("\nAll Day 08 Number of Islands tests passed successfully!");
    }
}
