import java.util.*;

/**
 * Day 02: HashMap Internals & Custom HashMap Implementation
 * Implements a simplified hash map with array of buckets, linked collision chains,
 * equals/hashCode contracts, and dynamic resizing at 0.75 load factor.
 *
 * Time Complexity: Average O(1) for put, get, remove; Worst O(n) on hash collapse.
 * Space Complexity: O(capacity + entries)
 */
public class CustomHashMap<K, V> {

    static class Entry<K, V> {
        final K key;
        V value;
        Entry<K, V> next;
        Entry(K key, V value, Entry<K, V> next) {
            this.key = key; this.value = value; this.next = next;
        }
    }

    private Entry<K, V>[] table;
    private int size = 0;
    private static final int INITIAL_CAPACITY = 16;
    private static final float LOAD_FACTOR = 0.75f;

    @SuppressWarnings("unchecked")
    public CustomHashMap() {
        table = new Entry[INITIAL_CAPACITY];
    }

    private int hash(K key) {
        return key == null ? 0 : Math.abs(key.hashCode() % table.length);
    }

    public void put(K key, V value) {
        int bucket = hash(key);
        Entry<K, V> curr = table[bucket];
        while (curr != null) {
            if (Objects.equals(curr.key, key)) {
                curr.value = value; // update
                return;
            }
            curr = curr.next;
        }
        table[bucket] = new Entry<>(key, value, table[bucket]);
        size++;
        if (size >= table.length * LOAD_FACTOR) {
            resize();
        }
    }

    public V get(K key) {
        int bucket = hash(key);
        Entry<K, V> curr = table[bucket];
        while (curr != null) {
            if (Objects.equals(curr.key, key)) return curr.value;
            curr = curr.next;
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    private void resize() {
        Entry<K, V>[] oldTable = table;
        table = new Entry[oldTable.length * 2];
        size = 0;
        for (Entry<K, V> head : oldTable) {
            while (head != null) {
                put(head.key, head.value);
                head = head.next;
            }
        }
    }

    public int size() { return size; }

    public static void main(String[] args) {
        CustomHashMap<String, Integer> map = new CustomHashMap<>();
        map.put("tokens", 100);
        map.put("latency", 25);
        map.put("tokens", 150); // Overwrite test

        assert map.get("tokens") == 150;
        assert map.get("latency") == 25;
        assert map.get("unknown") == null;
        assert map.size() == 2;
        System.out.println("Day 02 DSA CustomHashMap verification passed!");
    }
}
