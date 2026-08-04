import java.util.Arrays;

public class merge_sorted_array {
    // LeetCode #88 - Merge Sorted Array
    // Approach: Two Pointers from end O(m+n)
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int p1 = m - 1;
        int p2 = n - 1;
        int p  = m + n - 1;

        while (p2 >= 0) {
            if (p1 >= 0 && nums1[p1] > nums2[p2]) {
                nums1[p--] = nums1[p1--];
            } else {
                nums1[p--] = nums2[p2--];
            }
        }
    }

    public static void main(String[] args) {
        merge_sorted_array sol = new merge_sorted_array();

        int[] nums1 = {1, 2, 3, 0, 0, 0};
        sol.merge(nums1, 3, new int[]{2, 5, 6}, 3);
        System.out.println(Arrays.toString(nums1)); // [1, 2, 2, 3, 5, 6]

        int[] nums2 = {1};
        sol.merge(nums2, 1, new int[]{}, 0);
        System.out.println(Arrays.toString(nums2)); // [1]
    }
}
