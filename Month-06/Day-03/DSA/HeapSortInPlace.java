import java.util.Arrays;

public class HeapSortInPlace {
    public static void sort(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) siftDown(arr, i, n);
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            siftDown(arr, 0, i);
        }
    }

    private static void siftDown(int[] arr, int root, int size) {
        int largest = root, left = 2 * root + 1, right = 2 * root + 2;
        if (left < size && arr[left] > arr[largest]) largest = left;
        if (right < size && arr[right] > arr[largest]) largest = right;
        if (largest != root) {
            swap(arr, root, largest);
            siftDown(arr, largest, size);
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }

    public static void main(String[] args) {
        System.out.println("=== In-Place HeapSort Test ===");
        int[] arr = {12, 11, 13, 5, 6, 7};
        sort(arr);
        System.out.println("Sorted: " + Arrays.toString(arr));
        assert arr[0] == 5 && arr[arr.length - 1] == 13 : "Failed heapsort";
        System.out.println("HeapSort passed successfully!");
    }
}
