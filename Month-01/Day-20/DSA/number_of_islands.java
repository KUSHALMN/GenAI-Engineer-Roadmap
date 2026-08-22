import java.util.LinkedList;
import java.util.Queue;
import java.util.Arrays;

/**
 * Problem: Number of Islands (LeetCode 200)
 * 
 * Given an m x n 2D binary grid grid which represents a map of '1's (land)
 * and '0's (water), return the number of islands.
 * An island is surrounded by water and is formed by connecting adjacent lands 
 * horizontally or vertically.
 * 
 * Approaches:
 * 1. Depth-First Search (DFS) - Recursive:
 *    - Traverse each cell in grid.
 *    - When '1' is encountered, increment island count and trigger DFS to sink all connected '1's to '0' (or visited marker).
 *    - Time Complexity: O(M * N)
 *    - Space Complexity: O(M * N) worst case recursion stack (e.g. grid full of land).
 * 
 * 2. Breadth-First Search (BFS) - Iterative:
 *    - When '1' is found, push coordinate to Queue and iteratively sink neighbors.
 *    - Time Complexity: O(M * N)
 *    - Space Complexity: O(min(M, N)) queue size for diagonal expansion.
 * 
 * 3. Union-Find (Disjoint Set Union - DSU):
 *    - Treat each '1' cell as a node in DSU.
 *    - Connect adjacent '1's.
 *    - Time Complexity: O(M * N * α(M * N))
 *    - Space Complexity: O(M * N)
 */
public class number_of_islands {

    // ==========================================
    // Approach 1: Depth-First Search (DFS)
    // ==========================================
    public static int numIslandsDFS(char[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }

        int rows = grid.length;
        int cols = grid[0].length;
        int count = 0;

        // Make a clone to avoid mutating input if required
        char[][] copy = cloneGrid(grid);

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (copy[r][c] == '1') {
                    count++;
                    dfsSink(copy, r, c, rows, cols);
                }
            }
        }
        return count;
    }

    private static void dfsSink(char[][] grid, int r, int c, int rows, int cols) {
        // Boundary checks and water condition
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') {
            return;
        }

        // Mark current land as visited (sink to '0')
        grid[r][c] = '0';

        // Explore all 4 orthogonal directions
        dfsSink(grid, r + 1, c, rows, cols); // Down
        dfsSink(grid, r - 1, c, rows, cols); // Up
        dfsSink(grid, r, c + 1, rows, cols); // Right
        dfsSink(grid, r, c - 1, rows, cols); // Left
    }

    // ==========================================
    // Approach 2: Breadth-First Search (BFS)
    // ==========================================
    public static int numIslandsBFS(char[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }

        int rows = grid.length;
        int cols = grid[0].length;
        int count = 0;
        char[][] copy = cloneGrid(grid);

        int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (copy[r][c] == '1') {
                    count++;
                    copy[r][c] = '0'; // mark visited immediately upon queue offer
                    Queue<int[]> queue = new LinkedList<>();
                    queue.offer(new int[]{r, c});

                    while (!queue.isEmpty()) {
                        int[] cell = queue.poll();
                        int currR = cell[0];
                        int currC = cell[1];

                        for (int[] dir : directions) {
                            int nextR = currR + dir[0];
                            int nextC = currC + dir[1];

                            if (nextR >= 0 && nextR < rows && nextC >= 0 && nextC < cols && copy[nextR][nextC] == '1') {
                                copy[nextR][nextC] = '0'; // Sink before enqueueing to prevent duplicates
                                queue.offer(new int[]{nextR, nextC});
                            }
                        }
                    }
                }
            }
        }
        return count;
    }

    // ==========================================
    // Approach 3: Union-Find (Disjoint Set Union)
    // ==========================================
    static class UnionFind {
        private int[] parent;
        private int[] rank;
        private int count;

        public UnionFind(char[][] grid) {
            int rows = grid.length;
            int cols = grid[0].length;
            parent = new int[rows * cols];
            rank = new int[rows * cols];
            count = 0;

            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols; c++) {
                    if (grid[r][c] == '1') {
                        int id = r * cols + c;
                        parent[id] = id;
                        count++;
                    }
                }
            }
        }

        public int find(int i) {
            if (parent[i] != i) {
                parent[i] = find(parent[i]); // Path compression
            }
            return parent[i];
        }

        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX != rootY) {
                if (rank[rootX] > rank[rootY]) {
                    parent[rootY] = rootX;
                } else if (rank[rootX] < rank[rootY]) {
                    parent[rootX] = rootY;
                } else {
                    parent[rootY] = rootX;
                    rank[rootX]++;
                }
                count--;
            }
        }

        public int getCount() {
            return count;
        }
    }

    public static int numIslandsUnionFind(char[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }

        int rows = grid.length;
        int cols = grid[0].length;
        UnionFind uf = new UnionFind(grid);

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    int currentIdx = r * cols + c;

                    // Union with right neighbor
                    if (c + 1 < cols && grid[r][c + 1] == '1') {
                        uf.union(currentIdx, r * cols + (c + 1));
                    }
                    // Union with down neighbor
                    if (r + 1 < rows && grid[r + 1][c] == '1') {
                        uf.union(currentIdx, (r + 1) * cols + c);
                    }
                }
            }
        }
        return uf.getCount();
    }

    // Helper: Deep copy 2D char grid
    private static char[][] cloneGrid(char[][] grid) {
        char[][] copy = new char[grid.length][grid[0].length];
        for (int i = 0; i < grid.length; i++) {
            copy[i] = Arrays.copyOf(grid[i], grid[i].length);
        }
        return copy;
    }

    // ==========================================
    // Verification & Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     LeetCode 200: Number of Islands Test Suite  ");
        System.out.println("=================================================\n");

        // Test Case 1: Standard grid with 1 island
        char[][] grid1 = {
            {'1', '1', '1', '1', '0'},
            {'1', '1', '0', '1', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '0', '0', '0'}
        };
        runTest("Test Case 1 (Single Big Island)", grid1, 1);

        // Test Case 2: Multi-island grid (3 islands)
        char[][] grid2 = {
            {'1', '1', '0', '0', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '1', '0', '0'},
            {'0', '0', '0', '1', '1'}
        };
        runTest("Test Case 2 (3 Separate Islands)", grid2, 3);

        // Test Case 3: All water
        char[][] grid3 = {
            {'0', '0', '0'},
            {'0', '0', '0'}
        };
        runTest("Test Case 3 (All Water)", grid3, 0);

        // Test Case 4: All land
        char[][] grid4 = {
            {'1', '1'},
            {'1', '1'}
        };
        runTest("Test Case 4 (All Land)", grid4, 1);

        // Test Case 5: Checkerboard pattern
        char[][] grid5 = {
            {'1', '0', '1'},
            {'0', '1', '0'},
            {'1', '0', '1'}
        };
        runTest("Test Case 5 (Checkerboard - 5 Islands)", grid5, 5);

        System.out.println("\nAll Number of Islands test cases passed successfully!");
    }

    private static void runTest(String label, char[][] grid, int expected) {
        int resDFS = numIslandsDFS(grid);
        int resBFS = numIslandsBFS(grid);
        int resUF = numIslandsUnionFind(grid);

        boolean passed = (resDFS == expected) && (resBFS == expected) && (resUF == expected);
        System.out.printf("[%s] => Expected: %d | DFS: %d | BFS: %d | UF: %d => %s%n",
                label, expected, resDFS, resBFS, resUF, (passed ? "PASSED" : "FAILED"));

        if (!passed) {
            throw new AssertionError("Mismatch in test case: " + label);
        }
    }
}
