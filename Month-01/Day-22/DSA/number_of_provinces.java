import java.util.LinkedList;
import java.util.Queue;

/**
 * Problem: Number of Provinces (LeetCode 547)
 * 
 * There are n cities. Some of them are connected, while some are not. If city a is connected 
 * directly with city b, and city b is connected directly with city c, then city a is connected 
 * indirectly with city c.
 * 
 * A province is a group of directly or indirectly connected cities and no other cities outside of the group.
 * You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city 
 * are directly connected, and isConnected[i][j] = 0 otherwise.
 * 
 * Return the total number of provinces.
 * 
 * Approaches:
 * 1. Depth-First Search (DFS):
 *    - Maintain boolean[] visited array of size N.
 *    - Loop through each city i from 0 to N-1. If unvisited, increment province count and DFS explore all reachable cities.
 *    - Time Complexity: O(N^2)
 *    - Space Complexity: O(N) recursion stack + visited array.
 * 
 * 2. Breadth-First Search (BFS):
 *    - Iterative queue traversal over unvisited cities.
 *    - Time Complexity: O(N^2)
 *    - Space Complexity: O(N) queue + visited array.
 * 
 * 3. Disjoint Set Union (Union-Find / DSU):
 *    - Treat each city as an element. Union city i and city j when isConnected[i][j] == 1.
 *    - Track number of disjoint connected components.
 *    - Time Complexity: O(N^2 * α(N))
 *    - Space Complexity: O(N) parent and rank arrays.
 */
public class number_of_provinces {

    // ==========================================
    // Approach 1: Depth-First Search (DFS)
    // ==========================================
    public static int findCircleNumDFS(int[][] isConnected) {
        if (isConnected == null || isConnected.length == 0) return 0;

        int n = isConnected.length;
        boolean[] visited = new boolean[n];
        int provinces = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                provinces++;
                dfs(isConnected, i, visited);
            }
        }

        return provinces;
    }

    private static void dfs(int[][] isConnected, int city, boolean[] visited) {
        visited[city] = true;
        for (int neighbor = 0; neighbor < isConnected.length; neighbor++) {
            if (isConnected[city][neighbor] == 1 && !visited[neighbor]) {
                dfs(isConnected, neighbor, visited);
            }
        }
    }

    // ==========================================
    // Approach 2: Breadth-First Search (BFS)
    // ==========================================
    public static int findCircleNumBFS(int[][] isConnected) {
        if (isConnected == null || isConnected.length == 0) return 0;

        int n = isConnected.length;
        boolean[] visited = new boolean[n];
        int provinces = 0;
        Queue<Integer> queue = new LinkedList<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                provinces++;
                visited[i] = true;
                queue.offer(i);

                while (!queue.isEmpty()) {
                    int curr = queue.poll();
                    for (int neighbor = 0; neighbor < n; neighbor++) {
                        if (isConnected[curr][neighbor] == 1 && !visited[neighbor]) {
                            visited[neighbor] = true;
                            queue.offer(neighbor);
                        }
                    }
                }
            }
        }

        return provinces;
    }

    // ==========================================
    // Approach 3: Disjoint Set Union (Union-Find)
    // ==========================================
    static class UnionFind {
        private int[] parent;
        private int[] rank;
        private int count;

        public UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            count = n;
            for (int i = 0; i < n; i++) {
                parent[i] = i;
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

    public static int findCircleNumUnionFind(int[][] isConnected) {
        if (isConnected == null || isConnected.length == 0) return 0;

        int n = isConnected.length;
        UnionFind uf = new UnionFind(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j] == 1) {
                    uf.union(i, j);
                }
            }
        }

        return uf.getCount();
    }

    // ==========================================
    // Verification & Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   LeetCode 547: Number of Provinces Test Suite  ");
        System.out.println("=================================================\n");

        // Test 1: 3 cities, 2 connected (2 provinces)
        int[][] grid1 = {
            {1, 1, 0},
            {1, 1, 0},
            {0, 0, 1}
        };
        runTest("Test 1: 2 Provinces in 3 Cities", grid1, 2);

        // Test 2: 3 cities, completely disconnected (3 provinces)
        int[][] grid2 = {
            {1, 0, 0},
            {0, 1, 0},
            {0, 0, 1}
        };
        runTest("Test 2: All Disconnected (3 Provinces)", grid2, 3);

        // Test 3: 4 cities in single chain (1 province)
        int[][] grid3 = {
            {1, 1, 0, 0},
            {1, 1, 1, 0},
            {0, 1, 1, 1},
            {0, 0, 1, 1}
        };
        runTest("Test 3: Connected Chain (1 Province)", grid3, 1);

        // Test 4: Single isolated city
        int[][] grid4 = {{1}};
        runTest("Test 4: Single City", grid4, 1);

        System.out.println("\nAll Number of Provinces test cases passed successfully!");
    }

    private static void runTest(String label, int[][] isConnected, int expected) {
        int dfs = findCircleNumDFS(isConnected);
        int bfs = findCircleNumBFS(isConnected);
        int uf = findCircleNumUnionFind(isConnected);

        boolean ok = (dfs == expected && bfs == expected && uf == expected);
        System.out.printf("[%s] Expected: %d | DFS: %d | BFS: %d | UF: %d => %s%n",
                label, expected, dfs, bfs, uf, (ok ? "PASSED" : "FAILED"));

        if (!ok) {
            throw new AssertionError("Test failed for: " + label);
        }
    }
}
