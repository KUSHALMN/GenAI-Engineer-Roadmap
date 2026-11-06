import java.util.*;

/**
 * Day 20: Shortest Path — Network Delay Time
 * Problem: Given network travel times for directed edges times[i] = (u, v, w),
 * find how long it takes for all n nodes to receive a signal sent from node k.
 *
 * Algorithm:
 * - Dijkstra's algorithm using PriorityQueue.
 *
 * Time Complexity: O(E log V)
 * Space Complexity: O(V + E)
 */
public class NetworkDelayTime {

    public int networkDelayTime(int[][] times, int n, int k) {
        Map<Integer, List<int[]>> graph = new HashMap<>();
        for (int[] t : times) {
            graph.computeIfAbsent(t[0], x -> new ArrayList<>()).add(new int[]{t[1], t[2]});
        }

        // Min-heap storing {node, time}
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{k, 0});

        Map<Integer, Integer> dist = new HashMap<>();

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0];
            int d = curr[1];

            if (dist.containsKey(u)) continue;
            dist.put(u, d);

            if (graph.containsKey(u)) {
                for (int[] edge : graph.get(u)) {
                    int v = edge[0];
                    int w = edge[1];
                    if (!dist.containsKey(v)) {
                        pq.offer(new int[]{v, d + w});
                    }
                }
            }
        }

        if (dist.size() != n) return -1;
        int maxTime = 0;
        for (int d : dist.values()) maxTime = Math.max(maxTime, d);
        return maxTime;
    }

    public static void main(String[] args) {
        NetworkDelayTime solver = new NetworkDelayTime();
        int[][] times = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
        int n = 4, k = 2;
        int delay = solver.networkDelayTime(times, n, k);

        System.out.println("Network delay time from node 2: " + delay);
        assert delay == 2 : "Expected 2 (2 -> 3 -> 4 takes 1+1=2)";
        System.out.println("Day 20 DSA NetworkDelayTime verification passed!");
    }
}
