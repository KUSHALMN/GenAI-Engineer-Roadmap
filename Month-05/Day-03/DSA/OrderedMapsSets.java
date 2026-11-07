import java.util.*;

/**
 * Day 03: Java Sets & Ordered Maps (TreeSet & TreeMap)
 * Demonstrates Red-Black Tree backed ordered structures,
 * range querying (subMap, headSet, ceiling, floor), and O(log n) guarantees.
 *
 * Time Complexity: O(log n) for insert, search, delete, ceiling, floor.
 * Space Complexity: O(n)
 */
public class OrderedMapsSets {

    public static void main(String[] args) {
        // 1. TreeSet range operations
        TreeSet<Integer> scores = new TreeSet<>(Arrays.asList(45, 82, 10, 95, 63));
        assert scores.first() == 10;
        assert scores.last() == 95;
        assert scores.ceiling(80) == 82; // Smallest element >= 80
        assert scores.floor(50) == 45;   // Largest element <= 50

        // 2. TreeMap timestamp routing
        TreeMap<Long, String> auditLog = new TreeMap<>();
        auditLog.put(1000L, "User Login");
        auditLog.put(2000L, "Model Ingest");
        auditLog.put(3000L, "Fine-Tune Complete");

        // Submap within time range [1500, 3500]
        NavigableMap<Long, String> window = auditLog.subMap(1500L, true, 3500L, true);
        assert window.size() == 2;
        assert window.firstKey() == 2000L;

        System.out.println("TreeSet sorted view: " + scores);
        System.out.println("TreeMap submap window: " + window);
        System.out.println("Day 03 DSA OrderedMapsSets verification passed!");
    }
}
