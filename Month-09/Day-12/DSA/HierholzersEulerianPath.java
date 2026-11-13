package Month_09.Day_12.DSA;

import java.util.*;

/**
 * Day 12: Timed DSA Problem Set — Eulerian Path using Hierholzer's Algorithm.
 * Focus: LeetCode 332 (Reconstruct Itinerary) - O(E log E) Time, O(V + E) Space.
 */
public class HierholzersEulerianPath {

    public static List<String> findItinerary(List<List<String>> tickets) {
        Map<String, PriorityQueue<String>> graph = new HashMap<>();

        // Build directed multigraph with lexicographical ordering of destinations
        for (List<String> ticket : tickets) {
            String from = ticket.get(0);
            String to = ticket.get(1);
            graph.computeIfAbsent(from, k -> new PriorityQueue<>()).offer(to);
        }

        LinkedList<String> itinerary = new LinkedList<>();
        dfs("JFK", graph, itinerary);
        return itinerary;
    }

    private static void dfs(String airport, Map<String, PriorityQueue<String>> graph, LinkedList<String> itinerary) {
        PriorityQueue<String> destinations = graph.get(airport);
        while (destinations != null && !destinations.isEmpty()) {
            String next = destinations.poll(); // Consume directed edge
            dfs(next, graph, itinerary);
        }
        // Post-order insertion: add to head when backtrack occurs
        itinerary.addFirst(airport);
    }

    public static void main(String[] args) {
        List<List<String>> tickets1 = List.of(
            List.of("MUC", "LHR"),
            List.of("JFK", "MUC"),
            List.of("SFO", "SJC"),
            List.of("LHR", "SFO")
        );
        List<String> it1 = findItinerary(tickets1);
        assert it1.equals(List.of("JFK", "MUC", "LHR", "SFO", "SJC")) : "Test 1 Failed";

        List<List<String>> tickets2 = List.of(
            List.of("JFK", "SFO"),
            List.of("JFK", "ATL"),
            List.of("SFO", "ATL"),
            List.of("ATL", "JFK"),
            List.of("ATL", "SFO")
        );
        List<String> it2 = findItinerary(tickets2);
        assert it2.equals(List.of("JFK", "ATL", "JFK", "SFO", "ATL", "SFO")) : "Test 2 Failed";

        System.out.println("Day 12 Hierholzer's Eulerian Path verification passed.");
    }
}
