package Month_09.Day_04.DSA;

import java.util.*;

/**
 * Day 04: Timed DSA Problem Set — Prim's Minimum Spanning Tree (MST).
 * Focus: LeetCode 1584 (Min Cost to Connect All Points) - O(E log V) Time, O(V) Space.
 */
public class PrimsMinimumSpanningTree {

    public static int minCostConnectPoints(int[][] points) {
        int n = points.length;
        if (n <= 1) return 0;

        boolean[] inMST = new boolean[n];
        // PriorityQueue stores [cost, target_node]
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, 0}); // start at node 0 with 0 cost

        int totalCost = 0;
        int edgesUsed = 0;

        while (!pq.isEmpty() && edgesUsed < n) {
            int[] curr = pq.poll();
            int cost = curr[0];
            int u = curr[1];

            if (inMST[u]) continue;

            inMST[u] = true;
            totalCost += cost;
            edgesUsed++;

            for (int v = 0; v < n; v++) {
                if (!inMST[v]) {
                    int dist = Math.abs(points[u][0] - points[v][0]) + Math.abs(points[u][1] - points[v][1]);
                    pq.offer(new int[]{dist, v});
                }
            }
        }
        return totalCost;
    }

    public static void main(String[] args) {
        int[][] pts1 = {{0,0},{2,2},{3,10},{5,2},{7,0}};
        assert minCostConnectPoints(pts1) == 20 : "Test 1 Failed";

        int[][] pts2 = {{3,12},{-2,5},{-4,1}};
        assert minCostConnectPoints(pts2) == 18 : "Test 2 Failed";

        System.out.println("Day 04 Prim's Minimum Spanning Tree verification passed.");
    }
}
