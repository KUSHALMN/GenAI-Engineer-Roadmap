import java.util.*;

public class GraphTraversalRevision {
    // 1. LC 200: Number of Islands
    public static int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        int count = 0;
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[0].length; c++) {
                if (grid[r][c] == '1') {
                    dfsIsland(grid, r, c);
                    count++;
                }
            }
        }
        return count;
    }

    private static void dfsIsland(char[][] grid, int r, int c) {
        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != '1') return;
        grid[r][c] = '0';
        dfsIsland(grid, r + 1, c);
        dfsIsland(grid, r - 1, c);
        dfsIsland(grid, r, c + 1);
        dfsIsland(grid, r, c - 1);
    }

    // 2. LC 323: Number of Connected Components in Undirected Graph
    public static int countComponents(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        boolean[] visited = new boolean[n];
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                bfsComponent(i, adj, visited);
                components++;
            }
        }
        return components;
    }

    private static void bfsComponent(int src, List<List<Integer>> adj, boolean[] visited) {
        Queue<Integer> q = new ArrayDeque<>();
        q.offer(src);
        visited[src] = true;
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : adj.get(u)) {
                if (!visited[v]) {
                    visited[v] = true;
                    q.offer(v);
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("=== Graph Traversal Verification ===");
        char[][] grid = {
            {'1','1','0','0','0'},
            {'1','1','0','0','0'},
            {'0','0','1','0','0'},
            {'0','0','0','1','1'}
        };
        int islands = numIslands(grid);
        System.out.println("LC 200 (Number of Islands): " + islands + " (Expected 3)");
        assert islands == 3 : "LC 200 failed";

        int[][] edges = {{0,1}, {1,2}, {3,4}};
        int comp = countComponents(5, edges);
        System.out.println("LC 323 (Connected Components): " + comp + " (Expected 2)");
        assert comp == 2 : "LC 323 failed";
        System.out.println("Graph traversals passed!");
    }
}
