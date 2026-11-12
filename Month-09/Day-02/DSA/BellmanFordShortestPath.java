package Month_09.Day_02.DSA;

import java.util.Arrays;

/**
 * Day 02: Timed DSA Problem Set — Bellman-Ford Single-Source Shortest Path.
 * Focus: LeetCode 787 (Cheapest Flights Within K Stops) - O(K * E) Time, O(V) Space.
 */
public class BellmanFordShortestPath {

    // LeetCode 787: Cheapest Flights Within K Stops
    public static int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // Relax edges at most k + 1 times
        for (int i = 0; i <= k; i++) {
            int[] temp = Arrays.copyOf(dist, n);
            for (int[] flight : flights) {
                int u = flight[0], v = flight[1], cost = flight[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + cost < temp[v]) {
                    temp[v] = dist[u] + cost;
                }
            }
            dist = temp;
        }
        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }

    public static void main(String[] args) {
        int[][] flights = {
            {0, 1, 100},
            {1, 2, 100},
            {2, 0, 100},
            {1, 3, 600},
            {2, 3, 200}
        };

        assert findCheapestPrice(4, flights, 0, 3, 1) == 700 : "Test 1 Failed";
        assert findCheapestPrice(4, flights, 0, 3, 2) == 400 : "Test 2 Failed";
        assert findCheapestPrice(3, new int[][]{{0, 1, 100}, {1, 2, 100}, {0, 2, 500}}, 0, 2, 0) == 500 : "Test 3 Failed";

        System.out.println("Day 02 Bellman-Ford Shortest Path verification passed.");
    }
}
