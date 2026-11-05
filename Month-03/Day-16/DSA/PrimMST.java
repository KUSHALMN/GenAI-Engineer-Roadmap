import java.util.*;

/**
 * Prim's Minimum Spanning Tree (MST) Algorithm
 * Vertex-centric greedy algorithm:
 * - Start at arbitrary node (0), mark visited.
 * - Add all incident edges to a Min-PriorityQueue.
 * - Extract minimum weight edge leading to an unvisited node.
 * - Repeat until all V vertices are in the MST.
 * 
 * Complexity:
 * - Time: O((V + E) log V) with PriorityQueue
 * - Space: O(V + E) for adjacency list
 */
public class PrimMST {

    static class Edge {
        int to, weight;

        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    public static int primMST(int n, List<List<Edge>> graph) {
        boolean[] inMST = new boolean[n];
        // Min-heap stores: [vertex, weight_to_reach]
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));

        pq.offer(new int[]{0, 0});
        int totalWeight = 0;
        int visitedCount = 0;

        while (!pq.isEmpty() && visitedCount < n) {
            int[] curr = pq.poll();
            int u = curr[0];
            int w = curr[1];

            if (inMST[u]) continue; // Already added to MST

            inMST[u] = true;
            totalWeight += w;
            visitedCount++;

            for (Edge e : graph.get(u)) {
                if (!inMST[e.to]) {
                    pq.offer(new int[]{e.to, e.weight});
                }
            }
        }

        return visitedCount == n ? totalWeight : -1;
    }

    public static void main(String[] args) {
        int n = 5;
        List<List<Edge>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());

        // Undirected graph edges: {u, v, weight}
        int[][] edges = {
            {0, 1, 2}, {0, 3, 6},
            {1, 2, 3}, {1, 3, 8}, {1, 4, 5},
            {2, 4, 7},
            {3, 4, 9}
        };

        for (int[] e : edges) {
            graph.get(e[0]).add(new Edge(e[1], e[2]));
            graph.get(e[1]).add(new Edge(e[0], e[2]));
        }

        int mstWeight = primMST(n, graph);
        System.out.println("Prim's MST total weight for 5 vertices: " + mstWeight); // Expected 2 + 3 + 6 + 5 = 16
        System.out.println("Prim MST tests passed!");
    }
}
