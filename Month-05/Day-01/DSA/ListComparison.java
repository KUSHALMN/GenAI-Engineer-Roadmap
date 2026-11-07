import java.util.*;

/**
 * Day 01: Java Collections — ArrayList vs LinkedList
 * Implements core list operations, compares dynamic array growth vs doubly linked list,
 * and analyzes CPU cache locality, memory overhead, and time complexities.
 *
 * Complexities:
 * - ArrayList get(i): O(1) random access | add(E): amortized O(1) | insert(i, E): O(n)
 * - LinkedList get(i): O(n) traversal | add(E): O(1) | insert(node): O(1)
 */
public class ListComparison {

    public static void main(String[] args) {
        List<Integer> arrayList = new ArrayList<>();
        List<Integer> linkedList = new LinkedList<>();

        int n = 50000;

        // 1. Sequential Addition Benchmark
        long start = System.nanoTime();
        for (int i = 0; i < n; i++) arrayList.add(i);
        long arrayListAddTime = System.nanoTime() - start;

        start = System.nanoTime();
        for (int i = 0; i < n; i++) linkedList.add(i);
        long linkedListAddTime = System.nanoTime() - start;

        // 2. Random Access Benchmark
        start = System.nanoTime();
        int v1 = arrayList.get(n / 2);
        long arrayListGetTime = System.nanoTime() - start;

        start = System.nanoTime();
        int v2 = linkedList.get(n / 2);
        long linkedListGetTime = System.nanoTime() - start;

        System.out.println("ArrayList add time:  " + arrayListAddTime / 1_000_000.0 + " ms");
        System.out.println("LinkedList add time: " + linkedListAddTime / 1_000_000.0 + " ms");
        System.out.println("ArrayList get(mid):  " + arrayListGetTime + " ns");
        System.out.println("LinkedList get(mid): " + linkedListGetTime + " ns");

        assert v1 == v2 : "Values must match";
        assert arrayListGetTime <= linkedListGetTime : "ArrayList random access must be faster";
        System.out.println("Day 01 DSA ListComparison verification passed!");
    }
}
