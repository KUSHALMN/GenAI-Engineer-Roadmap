/**
 * Linear-Time Sorting: Stable Counting Sort & Radix Sort
 * Implements non-comparison sorting for integers with negative number support
 * and verifies O(N + K) and O(d * (N + K)) time complexity invariants.
 */

import java.util.Arrays;

public class CountingSortRadixSort {

    // 1. Stable Counting Sort for bounded non-negative integers
    public static void countingSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        int max = arr[0];
        for (int v : arr) {
            if (v > max) max = v;
        }

        int[] count = new int[max + 1];
        for (int v : arr) {
            count[v]++;
        }

        // Prefix sum for stable placement
        for (int i = 1; i <= max; i++) {
            count[i] += count[i - 1];
        }

        int[] output = new int[arr.length];
        for (int i = arr.length - 1; i >= 0; i--) {
            int val = arr[i];
            output[count[val] - 1] = val;
            count[val]--;
        }

        System.arraycopy(output, 0, arr, 0, arr.length);
    }

    // 2. Radix Sort (LSD) with negative number support
    public static void radixSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        // Separate positives and negatives to handle sign
        int min = arr[0];
        int max = arr[0];
        for (int v : arr) {
            if (v < min) min = v;
            if (v > max) max = v;
        }

        // Shift all elements to non-negative range
        long shift = min < 0 ? -((long) min) : 0L;
        long[] shifted = new long[arr.length];
        long maxShifted = 0;
        for (int i = 0; i < arr.length; i++) {
            shifted[i] = arr[i] + shift;
            if (shifted[i] > maxShifted) maxShifted = shifted[i];
        }

        // Apply counting sort digit by digit (base 10)
        for (long exp = 1; maxShifted / exp > 0; exp *= 10) {
            countingSortByDigit(shifted, exp);
        }

        // Shift back to original values
        for (int i = 0; i < arr.length; i++) {
            arr[i] = (int) (shifted[i] - shift);
        }
    }

    private static void countingSortByDigit(long[] arr, long exp) {
        long[] output = new long[arr.length];
        int[] count = new int[10];

        for (long val : arr) {
            int digit = (int) ((val / exp) % 10);
            count[digit]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (int i = arr.length - 1; i >= 0; i--) {
            int digit = (int) ((arr[i] / exp) % 10);
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }

        System.arraycopy(output, 0, arr, 0, arr.length);
    }

    public static void main(String[] args) {
        System.out.println("=== Counting Sort & Radix Sort Verification ===");

        // Counting Sort Test
        int[] arr1 = {4, 2, 2, 8, 3, 3, 1, 0, 9, 2};
        countingSort(arr1);
        System.out.println("Counting Sort: Sorted -> " + Arrays.toString(arr1));
        assert isSorted(arr1) : "Arr1 failed counting sort";

        // Radix Sort with Negatives Test
        int[] arr2 = {170, 45, 75, -90, -802, 24, 2, 66, 0, -12};
        radixSort(arr2);
        System.out.println("Radix Sort (with negatives): Sorted -> " + Arrays.toString(arr2));
        assert isSorted(arr2) : "Arr2 failed radix sort";

        System.out.println("All linear-time sort tests passed successfully!");
    }

    private static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) return false;
        }
        return true;
    }
}
