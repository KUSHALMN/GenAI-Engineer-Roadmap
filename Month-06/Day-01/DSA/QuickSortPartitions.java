import java.util.Arrays;

public class QuickSortPartitions {
    public static int lomutoPartition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    public static int hoarePartition(int[] arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1, j = high + 1;
        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            if (i >= j) return j;
            swap(arr, i, j);
        }
    }

    public static int[] dutchNationalFlag(int[] arr, int low, int high) {
        int pivot = arr[low];
        int lt = low, i = low + 1, gt = high;
        while (i <= gt) {
            if (arr[i] < pivot) swap(arr, lt++, i++);
            else if (arr[i] > pivot) swap(arr, i, gt--);
            else i++;
        }
        return new int[]{lt, gt};
    }

    public static void medianOfThree(int[] arr, int low, int high) {
        int mid = low + (high - low) / 2;
        if (arr[low] > arr[mid]) swap(arr, low, mid);
        if (arr[low] > arr[high]) swap(arr, low, high);
        if (arr[mid] > arr[high]) swap(arr, mid, high);
        swap(arr, low, mid);
    }

    public static void quickSort3Way(int[] arr, int low, int high) {
        if (low >= high) return;
        medianOfThree(arr, low, high);
        int[] bounds = dutchNationalFlag(arr, low, high);
        quickSort3Way(arr, low, bounds[0] - 1);
        quickSort3Way(arr, bounds[1] + 1, high);
    }

    public static void sort(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        quickSort3Way(arr, 0, arr.length - 1);
    }

    private static void swap(int[] arr, int i, int j) {
        int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }

    public static void main(String[] args) {
        System.out.println("=== QuickSort Partitions & Duplicate Handling Test ===");
        int[] arr1 = {24, 3, 45, 9, 56, 1, 99, 53, 12};
        sort(arr1);
        System.out.println("Sorted: " + Arrays.toString(arr1));
        assert isSorted(arr1) : "Arr1 failed to sort";

        int[] arr2 = {4, 2, 4, 1, 4, 2, 4, 3, 2, 1, 4, 4, 3};
        sort(arr2);
        System.out.println("Duplicates: " + Arrays.toString(arr2));
        assert isSorted(arr2) : "Arr2 failed to sort";
        System.out.println("All QuickSort tests passed!");
    }

    private static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) return false;
        }
        return true;
    }
}
