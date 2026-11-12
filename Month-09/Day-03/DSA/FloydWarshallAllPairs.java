package Month_09.Day_03.DSA;

import java.util.Arrays;

/**
 * Day 03: Timed DSA Problem Set — Floyd-Warshall All-Pairs Shortest Path.
 * Focus: LeetCode 1334 (Find City With Smallest Number of Neighbors) - O(V^3) Time, O(V^2) Space.
 */
public class FloydWarshallAllPairs {

    public static int findTheCity(int n, int[][] edges, int distanceThreshold) {
        int[][] dist = new int[n][n];
        int INF = 1000000000;

        for (int i = 0; i < n; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0;
        }

        for (int[] e : edges) {
            dist[e[0]][e[1]] = e[2];
            dist[e[1]][e[0]] = e[2];
        }

        // Floyd-Warshall dynamic programming: intermediate vertex k must be the outermost loop!
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }

        int minReachable = Integer.MAX_VALUE;
        int bestCity = -1;

        for (int i = 0; i < n; i++) {
            int reachable = 0;
            for (int j = 0; j < n; j++) {
                if (i != j && dist[i][j] <= distanceThreshold) {
                    reachable++;
                }
            }
            if (reachable <= minReachable) {
                minReachable = reachable;
                bestCity = i; // Pick greatest numerical index on tie
            }
        }
        return bestCity;
    }

    public static void main(String[] args) {
        int[][] edges1 = {{0,1,3},{1,2,1},{1,3,4},{2,3,1}};
        assert findTheCity(4, edges1, 4) == 3 : "Test 1 Failed";

        int[][] edges2 = {{0,1,2},{0,4,8},{1,2,3},{1,4,2},{2,3,1},{3,4,1}};
        assert findTheCity(5, edges2, 2) == 0 : "Test 2 Failed";

        System.out.println("Day 03 Floyd-Warshall All-Pairs Shortest Path verification passed.");
    }
}
