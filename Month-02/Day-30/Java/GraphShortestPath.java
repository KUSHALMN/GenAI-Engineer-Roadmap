import java.util.*;

/**
 * Day 30 DSA: Graph Shortest Path Algorithms
 * - LeetCode 743: Network Delay Time (Dijkstra's Algorithm with Min-Heap O(E log V))
 * - LeetCode 787: Cheapest Flights Within K Stops (Bellman-Ford / Modified BFS O(K * E))
 */
public class GraphShortestPath {

    // -------------------------------------------------------------
    // LC 743: Network Delay Time (Dijkstra)
    // -------------------------------------------------------------
    public static int networkDelayTime(int[][] times, int n, int k) {
        // Build adjacency list: node -> list of (neighbor, weight)
        Map<Integer, List<int[]>> graph = new HashMap<>();
        for (int[] edge : times) {
            graph.computeIfAbsent(edge[0], x -> new ArrayList<>()).add(new int[]{edge[1], edge[2]});
        }

        // PriorityQueue stores [node, distance_from_k]
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        minHeap.offer(new int[]{k, 0});

        Map<Integer, Integer> minDistance = new HashMap<>();

        while (!minHeap.isEmpty()) {
            int[] curr = minHeap.poll();
            int node = curr[0];
            int dist = curr[1];

            if (minDistance.containsKey(node)) continue;
            minDistance.put(node, dist);

            if (graph.containsKey(node)) {
                for (int[] next : graph.get(node)) {
                    int neighbor = next[0];
                    int edgeWeight = next[1];
                    if (!minDistance.containsKey(neighbor)) {
                        minHeap.offer(new int[]{neighbor, dist + edgeWeight});
                    }
                }
            }
        }

        if (minDistance.size() != n) return -1; // Not all nodes reached
        int maxTime = 0;
        for (int d : minDistance.values()) {
            maxTime = Math.max(maxTime, d);
        }
        return maxTime;
    }

    // -------------------------------------------------------------
    // LC 787: Cheapest Flights Within K Stops (Bellman-Ford)
    // -------------------------------------------------------------
    public static int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] prices = new int[n];
        Arrays.fill(prices, Integer.MAX_VALUE);
        prices[src] = 0;

        // Perform at most k + 1 edge relaxations
        for (int i = 0; i <= k; i++) {
            int[] tempPrices = Arrays.copyOf(prices, n);
            for (int[] flight : flights) {
                int from = flight[0];
                int to = flight[1];
                int price = flight[2];

                if (prices[from] != Integer.MAX_VALUE && prices[from] + price < tempPrices[to]) {
                    tempPrices[to] = prices[from] + price;
                }
            }
            prices = tempPrices;
        }

        return prices[dst] == Integer.MAX_VALUE ? -1 : prices[dst];
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 30: Graph Shortest Path DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 743 Network Delay Time
        int[][] times = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
        int n = 4, k = 2;
        int delay = networkDelayTime(times, n, k);
        System.out.println("LC 743 (Network Delay Time from node 2): " + delay);
        assert delay == 2 : "LC 743 Failed";

        // Test 2: LC 787 Cheapest Flights within K stops
        int[][] flights = {
            {0, 1, 100},
            {1, 2, 100},
            {2, 0, 100},
            {1, 3, 600},
            {2, 3, 200}
        };
        int cheapPrice = findCheapestPrice(4, flights, 0, 3, 1);
        System.out.println("LC 787 (Cheapest Flights within 1 stop): " + cheapPrice);
        assert cheapPrice == 700 : "LC 787 Failed";

        System.out.println("\nAll Java Graph Shortest Path tests executed successfully! [OK]");
    }
}
