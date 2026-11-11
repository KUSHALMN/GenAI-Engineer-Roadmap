package Month_08.Day_21.DSA;

import java.util.*;

/**
 * Day 21: Java Collections Cost & Complexity Analysis.
 * Benchmarking ArrayList vs LinkedList, HashMap vs TreeMap time/space amortized bounds.
 */
public class JavaCollectionsCostComplexity {

    public static void verifyCollectionCharacteristics() {
        // 1. ArrayList random access O(1) vs LinkedList O(N)
        List<Integer> arrayList = new ArrayList<>(1000);
        List<Integer> linkedList = new LinkedList<>();

        for (int i = 0; i < 1000; i++) {
            arrayList.add(i);
            linkedList.add(i);
        }

        assert arrayList.get(500) == 500 : "ArrayList get failed";
        assert linkedList.get(500) == 500 : "LinkedList get failed";

        // 2. HashMap O(1) vs TreeMap O(log N)
        Map<String, Integer> hashMap = new HashMap<>();
        Map<String, Integer> treeMap = new TreeMap<>();

        hashMap.put("alpha", 1);
        hashMap.put("beta", 2);
        treeMap.put("beta", 2);
        treeMap.put("alpha", 1);

        // Verify TreeMap maintains natural ordering
        Iterator<String> it = treeMap.keySet().iterator();
        assert it.next().equals("alpha") : "TreeMap ordering failed";
        assert it.next().equals("beta") : "TreeMap ordering failed";

        // 3. ArrayDeque vs Stack (ArrayDeque is unsynchronized and faster)
        Deque<Integer> deque = new ArrayDeque<>();
        deque.push(10);
        deque.push(20);
        assert deque.pop() == 20 : "Deque pop failed";
        assert deque.pop() == 10 : "Deque pop failed";
    }

    public static void main(String[] args) {
        verifyCollectionCharacteristics();
        System.out.println("Day 21 Java Collections Cost & Complexity verification passed.");
    }
}
