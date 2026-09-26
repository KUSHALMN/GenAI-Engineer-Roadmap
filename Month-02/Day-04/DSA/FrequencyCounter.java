import java.util.*;

/**
 * Frequency Counter & Top-K Frequent Pattern in Java
 * Topic: Hash Table, Frequency Map, Min-Heap
 *
 * Demonstrates:
 *   1. O(N) frequency counting with HashMap.
 *   2. O(N log K) Top-K elements extraction using a Min-Heap.
 */
public class FrequencyCounter {

    public static Map<String, Integer> countFrequencies(String[] items) {
        Map<String, Integer> freqMap = new HashMap<>();
        for (String item : items) {
            freqMap.put(item, freqMap.getOrDefault(item, 0) + 1);
        }
        return freqMap;
    }

    public static List<String> topKFrequent(String[] items, int k) {
        Map<String, Integer> count = countFrequencies(items);

        PriorityQueue<String> heap = new PriorityQueue<>(
            (w1, w2) -> count.get(w1).equals(count.get(w2)) ?
                w2.compareTo(w1) : count.get(w1) - count.get(w2)
        );

        for (String word : count.keySet()) {
            heap.offer(word);
            if (heap.size() > k) {
                heap.poll();
            }
        }

        List<String> result = new ArrayList<>();
        while (!heap.isEmpty()) {
            result.add(heap.poll());
        }
        Collections.reverse(result);
        return result;
    }

    public static void main(String[] args) {
        String[] tokens = {"llm", "cache", "token", "llm", "prompt", "llm", "cache", "cost"};
        Map<String, Integer> freqs = countFrequencies(tokens);
        System.out.println("Frequencies: " + freqs);

        List<String> top2 = topKFrequent(tokens, 2);
        System.out.println("Top 2: " + top2);
    }
}
