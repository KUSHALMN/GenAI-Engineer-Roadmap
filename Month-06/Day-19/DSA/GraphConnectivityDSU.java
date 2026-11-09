import java.util.*;

public class GraphConnectivityDSU {
    // 1. LC 684: Redundant Connection (DSU with Path Compression)
    public static int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        int[] parent = new int[n + 1];
        for (int i = 1; i <= n; i++) parent[i] = i;

        for (int[] e : edges) {
            int rootU = find(parent, e[0]);
            int rootV = find(parent, e[1]);
            if (rootU == rootV) return e; // Cycle detected
            parent[rootU] = rootV;
        }
        return new int[0];
    }

    private static int find(int[] parent, int i) {
        if (parent[i] != i) parent[i] = find(parent, parent[i]);
        return parent[i];
    }

    // 2. LC 785: Is Graph Bipartite (BFS 2-Coloring)
    public static boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] colors = new int[n]; // 0: uncolored, 1: red, -1: blue

        for (int i = 0; i < n; i++) {
            if (colors[i] != 0) continue;
            Queue<Integer> q = new ArrayDeque<>();
            q.offer(i);
            colors[i] = 1;

            while (!q.isEmpty()) {
                int u = q.poll();
                for (int v : graph[u]) {
                    if (colors[v] == 0) {
                        colors[v] = -colors[u];
                        q.offer(v);
                    } else if (colors[v] == colors[u]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println("=== Graph Connectivity DSU Verification ===");
        int[][] edges = {{1, 2}, {1, 3}, {2, 3}};
        int[] redundant = findRedundantConnection(edges);
        System.out.println("LC 684 (Redundant Edge): " + Arrays.toString(redundant));
        assert redundant[0] == 2 && redundant[1] == 3 : "LC 684 failed";

        int[][] bipGraph = {{1, 3}, {0, 2}, {1, 3}, {0, 2}};
        assert isBipartite(bipGraph) : "LC 785 failed";
        System.out.println("LC 785 (Is Bipartite): true");
        System.out.println("DSU and Bipartite tests passed!");
    }
}
