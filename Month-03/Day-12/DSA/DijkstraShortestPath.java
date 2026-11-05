import java.util.*;

/**
 * Dijkstra's Single-Source Shortest Path Algorithm
 * LeetCode 743 - Network Delay Time
 * Invariant:
 * Greedily selects the unvisited node with minimal cumulative distance.
 * Complexity:
 * - Time: O((V + E) log V) with Min-PriorityQueue
 * - Space: O(V + E) for adjacency list + distance array
 */
public class DijkstraShortestPath {

    public static int networkDelayTime(int[][] times, int n, int k) {
        // Build adjacency list: node -> list of [neighbor, weight]
        Map<Integer, List<int[]>> graph = new HashMap<>();
        for (int[] time : times) {
            graph.computeIfAbsent(time[0], x -> new ArrayList<>()).add(new int[]{time[1], time[2]});
        }

        // Distances initialized to infinity
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;

        // Min-heap storing [node, current_distance]
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{k, 0});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0];
            int d = curr[1];

            if (d > dist[u]) continue; // Stale heap entry

            if (graph.containsKey(u)) {
                for (int[] edge : graph.get(u)) {
                    int v = edge[0];
                    int weight = edge[1];
                    if (dist[u] + weight < dist[v]) {
                        dist[v] = dist[u] + weight;
                        pq.offer(new int[]{v, dist[v]});
                    }
                }
            }
        }

        // Find max delay to reach all nodes from 1 to n
        int maxDelay = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) {
                return -1; // Node unreachable
            }
            maxDelay = Math.max(maxDelay, dist[i]);
        }

        return maxDelay;
    }

    public static void main(String[] args) {
        int[][] times = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
        int n = 4, k = 2;
        int delay = networkDelayTime(times, n, k);
        System.out.println("Network delay time for n=4, source=2: " + delay); // Expected 2

        int[][] unreachable = {{1, 2, 1}};
        System.out.println("Network delay when disconnected: " + networkDelayTime(unreachable, 2, 2)); // Expected -1

        System.out.println("Dijkstra tests passed!");
    }
}
