import java.util.*;

/**
 * Day 08: Amortized Complexity Analysis — Custom Dynamic Array
 * Implements a resizing array with doubling capacity strategy,
 * proving amortized O(1) insertion time using the Accounting / Aggregate method.
 */
public class DynamicArrayAmortized {

    private int[] data;
    private int size = 0;
    private int capacity = 2;
    private long totalOperationsCount = 0;

    public DynamicArrayAmortized() {
        data = new int[capacity];
    }

    public void add(int val) {
        totalOperationsCount++; // standard 1 cost
        if (size == capacity) {
            // Resize (double capacity)
            int newCap = capacity * 2;
            int[] newData = new int[newCap];
            for (int i = 0; i < size; i++) {
                newData[i] = data[i];
                totalOperationsCount++; // copy cost
            }
            data = newData;
            capacity = newCap;
        }
        data[size++] = val;
    }

    public int size() { return size; }
    public int capacity() { return capacity; }
    public double averageCostPerInsert() { return (double) totalOperationsCount / size; }

    public static void main(String[] args) {
        DynamicArrayAmortized arr = new DynamicArrayAmortized();
        int n = 10000;
        for (int i = 0; i < n; i++) {
            arr.add(i);
        }

        System.out.println("Total insertions: " + arr.size());
        System.out.println("Final capacity:   " + arr.capacity());
        System.out.println("Amortized operations per insertion: " + String.format("%.2f", arr.averageCostPerInsert()));

        assert arr.averageCostPerInsert() < 3.0 : "Amortized cost must be bounded by constant ~3";
        System.out.println("Day 08 DSA DynamicArrayAmortized verification passed!");
    }
}
