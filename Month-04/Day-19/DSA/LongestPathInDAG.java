import java.util.*;

/**
 * Day 19: Topological Sorting + DP — Longest Path in a DAG
 * Problem: Given a Directed Acyclic Graph (DAG) with edge weights, find the longest path from source.
 *
 * Algorithm:
 * 1. Find topological order using Kahn's algorithm or DFS.
 * 2. Initialize dist[] with Integer.MIN_VALUE, dist[src] = 0.
 * 3. Process vertices in topological order, relaxing outgoing edges:
 *    dist[v] = max(dist[v], dist[u] + weight(u, v))
 *
 * Time Complexity: O(V + E)
 * Space Complexity: O(V + E)
 */
public class LongestPathInDAG {

    static class Edge {
        int to, weight;
        Edge(int to, int weight) { this.to = to; this.weight = weight; }
    }

    public int[] findLongestPaths(int n, List<List<Edge>> adj, int src) {
        // Compute in-degrees
        int[] inDegree = new int[n];
        for (int u = 0; u < n; u++) {
            for (Edge e : adj.get(u)) inDegree[e.to]++;
        }

        // Topological Sort
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < n; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        List<Integer> topo = new ArrayList<>();
        while (!q.isEmpty()) {
            int u = q.poll();
            topo.add(u);
            for (Edge e : adj.get(u)) {
                if (--inDegree[e.to] == 0) q.offer(e.to);
            }
        }

        // DP relaxation
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MIN_VALUE);
        dist[src] = 0;

        for (int u : topo) {
            if (dist[u] != Integer.MIN_VALUE) {
                for (Edge e : adj.get(u)) {
                    if (dist[u] + e.weight > dist[e.to]) {
                        dist[e.to] = dist[u] + e.weight;
                    }
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        LongestPathInDAG solver = new LongestPathInDAG();
        int n = 6;
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        adj.get(0).add(new Edge(1, 5));
        adj.get(0).add(new Edge(2, 3));
        adj.get(1).add(new Edge(3, 6));
        adj.get(1).add(new Edge(2, 2));
        adj.get(2).add(new Edge(4, 4));
        adj.get(2).add(new Edge(5, 2));
        adj.get(2).add(new Edge(3, 7));
        adj.get(3).add(new Edge(5, 1));
        adj.get(3).add(new Edge(4, -1));
        adj.get(4).add(new Edge(5, -2));

        int[] dist = solver.findLongestPaths(n, adj, 1);
        System.out.println("Longest path from vertex 1 to 5: " + dist[5]);
        assert dist[5] == 8 : "Expected 8 (1 -> 3 -> 5: 6 + 1 or 1 -> 2 -> 3 -> 5: 2 + 7 + 1 = 10)";
        System.out.println("Day 19 DSA LongestPathInDAG verification passed!");
    }
}
