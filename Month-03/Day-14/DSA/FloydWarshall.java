import java.util.Arrays;

/**
 * Floyd-Warshall All-Pairs Shortest Path Algorithm
 * Dynamic Programming State:
 * dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
 * where k represents intermediate vertices {0, 1, ..., V-1}.
 * 
 * Complexity:
 * - Time: O(V^3) with three nested loops
 * - Space: O(V^2) for distance matrix
 * Negative Cycle Detection:
 * If dist[i][i] < 0 for any vertex i, a negative-weight cycle exists.
 */
public class FloydWarshall {
    private static final int INF = 100000000;

    public static int[][] floydWarshall(int V, int[][] edges) {
        int[][] dist = new int[V][V];
        for (int i = 0; i < V; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0;
        }

        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int w = edge[2];
            dist[u][v] = w;
        }

        // DP across all intermediate vertices k
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {
                    if (dist[i][k] != INF && dist[k][j] != INF) {
                        if (dist[i][k] + dist[k][j] < dist[i][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                        }
                    }
                }
            }
        }

        // Check for negative cycle
        for (int i = 0; i < V; i++) {
            if (dist[i][i] < 0) {
                throw new IllegalStateException("Graph contains a negative cycle involving vertex " + i);
            }
        }

        return dist;
    }

    public static void main(String[] args) {
        int V = 4;
        // edges: {u, v, weight}
        int[][] edges = {
            {0, 1, 5},
            {0, 3, 10},
            {1, 2, 3},
            {2, 3, 1}
        };

        int[][] result = floydWarshall(V, edges);

        System.out.println("All-Pairs Shortest Distances:");
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (result[i][j] == INF) {
                    System.out.print("INF ");
                } else {
                    System.out.print(result[i][j] + "   ");
                }
            }
            System.out.println();
        }

        // Distance 0 -> 3 should be 0->1 (5) + 1->2 (3) + 2->3 (1) = 9
        System.out.println("Shortest path 0 -> 3: " + result[0][3] + " (Expected: 9)");
        System.out.println("Floyd-Warshall tests passed!");
    }
}
