import java.util.Arrays;

public class MergeSortStable {
    public static long sortAndCountInversions(int[] arr) {
        if (arr == null || arr.length <= 1) return 0;
        int[] aux = new int[arr.length];
        return mergeSort(arr, aux, 0, arr.length - 1);
    }

    private static long mergeSort(int[] arr, int[] aux, int low, int high) {
        if (low >= high) return 0;
        int mid = low + (high - low) / 2;
        long inv = mergeSort(arr, aux, low, mid);
        inv += mergeSort(arr, aux, mid + 1, high);
        inv += merge(arr, aux, low, mid, high);
        return inv;
    }

    private static long merge(int[] arr, int[] aux, int low, int mid, int high) {
        System.arraycopy(arr, low, aux, low, high - low + 1);
        int i = low, j = mid + 1, k = low;
        long inv = 0;
        while (i <= mid && j <= high) {
            if (aux[i] <= aux[j]) {
                arr[k++] = aux[i++];
            } else {
                arr[k++] = aux[j++];
                inv += (mid - i + 1);
            }
        }
        while (i <= mid) arr[k++] = aux[i++];
        while (j <= high) arr[k++] = aux[j++];
        return inv;
    }

    public static void main(String[] args) {
        System.out.println("=== MergeSort Stable & Inversion Count Tests ===");
        int[] arr1 = {8, 4, 2, 1};
        long inv1 = sortAndCountInversions(arr1);
        System.out.println("Sorted: " + Arrays.toString(arr1) + " | Inversions: " + inv1);
        assert inv1 == 6 : "Expected 6 inversions";
        System.out.println("MergeSort tests passed successfully!");
    }
}
