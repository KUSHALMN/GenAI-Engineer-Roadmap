import java.util.*;

/**
 * Problem: K Closest Points to Origin (LeetCode 973)
 * 
 * Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane
 * and an integer k, return the k closest points to the origin (0, 0).
 * Distance is calculated as Euclidean distance: sqrt(x^2 + y^2).
 * Comparing squared distances x^2 + y^2 avoids floating point inaccuracies.
 * 
 * Approaches:
 * 1. Max-Heap of size K:
 *    - Maintain a Max-Heap of size K based on squared Euclidean distance.
 *    - If size > K, remove the farthest point (top of Max-Heap).
 *    - Time Complexity: O(N log K)
 *    - Space Complexity: O(K)
 * 
 * 2. QuickSelect:
 *    - Partition points based on squared distance relative to origin.
 *    - Average Time Complexity: O(N)
 *    - Worst Case: O(N^2)
 *    - Space Complexity: O(1) iterative
 */
public class k_closest_points {

    // Approach 1: Max-Heap (PriorityQueue)
    public static int[][] kClosestHeap(int[][] points, int k) {
        if (points == null || points.length == 0 || k <= 0) {
            return new int[0][0];
        }

        // Max-Heap: comparator orders points with largest distance first
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
            (p1, p2) -> Integer.compare(distSq(p2), distSq(p1))
        );

        for (int[] point : points) {
            maxHeap.offer(point);
            if (maxHeap.size() > k) {
                maxHeap.poll(); // Evict farthest point
            }
        }

        int[][] result = new int[k][2];
        for (int i = 0; i < k; i++) {
            result[i] = maxHeap.poll();
        }

        return result;
    }

    // Approach 2: QuickSelect (O(N) Average)
    public static int[][] kClosestQuickSelect(int[][] points, int k) {
        if (points == null || points.length == 0 || k <= 0) {
            return new int[0][0];
        }

        int left = 0;
        int right = points.length - 1;
        Random rand = new Random();

        while (left <= right) {
            int pivotIndex = left + rand.nextInt(right - left + 1);
            int finalPivotIndex = partition(points, left, right, pivotIndex);

            if (finalPivotIndex == k) {
                break;
            } else if (finalPivotIndex < k) {
                left = finalPivotIndex + 1;
            } else {
                right = finalPivotIndex - 1;
            }
        }

        return Arrays.copyOfRange(points, 0, k);
    }

    private static int partition(int[][] points, int left, int right, int pivotIndex) {
        int pivotDist = distSq(points[pivotIndex]);
        swap(points, pivotIndex, right);
        int storeIndex = left;

        for (int i = left; i < right; i++) {
            if (distSq(points[i]) < pivotDist) {
                swap(points, storeIndex, i);
                storeIndex++;
            }
        }

        swap(points, storeIndex, right);
        return storeIndex;
    }

    private static void swap(int[][] arr, int i, int j) {
        int[] temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private static int distSq(int[] point) {
        return point[0] * point[0] + point[1] * point[1];
    }

    public static void main(String[] args) {
        System.out.println("=== K Closest Points to Origin ===");

        int[][] points1 = {{1, 3}, {-2, 2}};
        int k1 = 1;

        int[][] points2 = {{3, 3}, {5, -1}, {-2, 4}};
        int k2 = 2;

        int[][] points3 = {{0, 1}, {1, 0}};
        int k3 = 2;

        System.out.println("\nTest 1 (k = " + k1 + "):");
        System.out.println("Heap:        " + Arrays.deepToString(kClosestHeap(points1, k1)));
        System.out.println("QuickSelect: " + Arrays.deepToString(kClosestQuickSelect(points1, k1)));

        System.out.println("\nTest 2 (k = " + k2 + "):");
        System.out.println("Heap:        " + Arrays.deepToString(kClosestHeap(points2, k2)));
        System.out.println("QuickSelect: " + Arrays.deepToString(kClosestQuickSelect(points2, k2)));

        System.out.println("\nTest 3 (k = " + k3 + "):");
        System.out.println("Heap:        " + Arrays.deepToString(kClosestHeap(points3, k3)));
        System.out.println("QuickSelect: " + Arrays.deepToString(kClosestQuickSelect(points3, k3)));

        System.out.println("\nAll tests executed successfully!");
    }
}
