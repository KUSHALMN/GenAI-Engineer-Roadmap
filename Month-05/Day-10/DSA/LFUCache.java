import java.util.*;

/**
 * Day 10: Advanced Design — LFU Cache (Least Frequently Used)
 * Implements an O(1) LFU cache using:
 * 1. keyToVal & keyToFreq maps
 * 2. freqToKeys map maintaining LinkedHashSet for each frequency.
 *
 * Time Complexity: O(1) for get and put
 * Space Complexity: O(capacity)
 */
public class LFUCache {

    private final int capacity;
    private int minFreq = 0;
    private final Map<Integer, Integer> vals = new HashMap<>();
    private final Map<Integer, Integer> counts = new HashMap<>();
    private final Map<Integer, LinkedHashSet<Integer>> lists = new HashMap<>();

    public LFUCache(int capacity) {
        this.capacity = capacity;
        lists.put(1, new LinkedHashSet<>());
    }

    public int get(int key) {
        if (!vals.containsKey(key)) return -1;
        int count = counts.get(key);
        counts.put(key, count + 1);
        lists.get(count).remove(key);

        if (count == minFreq && lists.get(count).isEmpty()) {
            minFreq++;
        }
        lists.computeIfAbsent(count + 1, k -> new LinkedHashSet<>()).add(key);
        return vals.get(key);
    }

    public void put(int key, int value) {
        if (capacity <= 0) return;

        if (vals.containsKey(key)) {
            vals.put(key, value);
            get(key); // Bump frequency
            return;
        }

        if (vals.size() >= capacity) {
            int evict = lists.get(minFreq).iterator().next();
            lists.get(minFreq).remove(evict);
            vals.remove(evict);
            counts.remove(evict);
        }

        vals.put(key, value);
        counts.put(key, 1);
        minFreq = 1;
        lists.get(1).add(key);
    }

    public static void main(String[] args) {
        LFUCache lfu = new LFUCache(2);
        lfu.put(1, 1);
        lfu.put(2, 2);
        assert lfu.get(1) == 1; // 1 has freq 2
        lfu.put(3, 3);          // Evicts key 2 (freq 1)
        assert lfu.get(2) == -1;
        assert lfu.get(3) == 3;
        System.out.println("Day 10 DSA LFUCache verification passed!");
    }
}
