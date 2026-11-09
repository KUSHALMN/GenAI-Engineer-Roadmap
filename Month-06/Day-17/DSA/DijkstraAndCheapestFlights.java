import java.util.*;

public class DijkstraAndCheapestFlights {
    // 1. LC 743: Network Delay Time (Dijkstra's Algorithm)
    public static int networkDelayTime(int[][] times, int n, int k) {
        Map<Integer, List<int[]>> graph = new HashMap<>();
        for (int[] t : times) {
            graph.computeIfAbsent(t[0], x -> new ArrayList<>()).add(new int[]{t[1], t[2]});
        }
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{k, 0});
        Map<Integer, Integer> dist = new HashMap<>();

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0], d = curr[1];
            if (dist.containsKey(u)) continue;
            dist.put(u, d);
            if (graph.containsKey(u)) {
                for (int[] next : graph.get(u)) {
                    int v = next[0], w = next[1];
                    if (!dist.containsKey(v)) {
                        pq.offer(new int[]{v, d + w});
                    }
                }
            }
        }

        if (dist.size() != n) return -1;
        int maxDist = 0;
        for (int d : dist.values()) maxDist = Math.max(maxDist, d);
        return maxDist;
    }

    public static void main(String[] args) {
        System.out.println("=== Dijkstra Shortest Path Verification ===");
        int[][] times = {{2,1,1}, {2,3,1}, {3,4,1}};
        int delay = networkDelayTime(times, 4, 2);
        System.out.println("LC 743 (Network Delay Time from node 2): " + delay + " (Expected 2)");
        assert delay == 2 : "LC 743 failed";
        System.out.println("Dijkstra passed!");
    }
}
