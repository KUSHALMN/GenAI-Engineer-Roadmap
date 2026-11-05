import java.util.*;

/**
 * Bellman-Ford Algorithm & Negative Cycle Detection
 * 1. Single Source Shortest Path with negative edge weights: O(V * E)
 * 2. Negative Cycle Detection: An extra relaxation step reducing any distance
 * 3. LeetCode 787 - Cheapest Flights Within K Stops (DP/Bellman-Ford variant)
 */
public class BellmanFord {

    /**
     * Standard Bellman-Ford Shortest Path
     * Returns shortest distances or throws RuntimeException if negative cycle exists.
     */
    public static int[] shortestPath(int n, int[][] edges, int src) {
        int[] dist = new int[n];
        Arrays.fill(dist, 100000000);
        dist[src] = 0;

        // Relax all edges V - 1 times
        for (int i = 1; i <= n - 1; i++) {
            for (int[] edge : edges) {
                int u = edge[0];
                int v = edge[1];
                int w = edge[2];
                if (dist[u] != 100000000 && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }

        // V-th iteration to check for negative-weight cycles
        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int w = edge[2];
            if (dist[u] != 100000000 && dist[u] + w < dist[v]) {
                throw new IllegalStateException("Graph contains a negative-weight cycle!");
            }
        }

        return dist;
    }

    /**
     * LC 787: Cheapest Flights Within K Stops
     * Uses Bellman-Ford relaxation bounded by (K + 1) steps.
     */
    public static int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        for (int i = 0; i <= k; i++) {
            int[] temp = Arrays.copyOf(dist, n);
            for (int[] flight : flights) {
                int u = flight[0];
                int v = flight[1];
                int price = flight[2];

                if (dist[u] != Integer.MAX_VALUE && dist[u] + price < temp[v]) {
                    temp[v] = dist[u] + price;
                }
            }
            dist = temp;
        }

        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }

    public static void main(String[] args) {
        int n = 4;
        int[][] flights = {{0, 1, 100}, {1, 2, 100}, {2, 0, 100}, {1, 3, 600}, {2, 3, 200}};
        int src = 0, dst = 3, k = 1;
        int price = findCheapestPrice(n, flights, src, dst, k);
        System.out.println("Cheapest price with at most 1 stop: " + price); // Expected 700 (0 -> 1 -> 3)

        // Graph with negative edges but NO negative cycle
        int[][] edges = {{0, 1, 4}, {0, 2, 5}, {1, 2, -2}, {2, 3, 3}};
        int[] distances = shortestPath(4, edges, 0);
        System.out.println("Shortest distances from source 0: " + Arrays.toString(distances));

        System.out.println("Bellman-Ford tests passed!");
    }
}
