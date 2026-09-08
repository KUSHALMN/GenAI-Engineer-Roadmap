/**
 * Problem: Median of Two Sorted Arrays (LeetCode 4 - Hard / Legendary FAANG Problem)
 * 
 * Given two sorted arrays nums1 and nums2 of size m and n respectively,
 * return the median of the two sorted arrays.
 * 
 * The overall run time complexity should be O(log (m+n)).
 * 
 * Optimal Approach: Binary Search on the Smaller Array Partition
 * - Ensure nums1 is smaller or equal in length to nums2 (m <= n).
 * - Partition both arrays such that:
 *   Left half elements count == Right half elements count (or +1 for odd total length).
 *   Max of Left half <= Min of Right half:
 *     maxLeftA <= minRightB AND maxLeftB <= minRightA
 * - Binary search boundary `i` in [0, m], and compute `j = (m + n + 1) / 2 - i`.
 * - If maxLeftA > minRightB: move partition left (`high = i - 1`).
 * - If maxLeftB > minRightA: move partition right (`low = i + 1`).
 * 
 * Complexity:
 * - Time Complexity: O(log(min(m, n)))
 * - Space Complexity: O(1)
 */
public class median_two_sorted_arrays {

    public static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Ensure nums1 is the smaller array to minimize binary search range
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.length;
        int n = nums2.length;
        int low = 0;
        int high = m;

        while (low <= high) {
            int partitionA = (low + high) / 2;
            int partitionB = (m + n + 1) / 2 - partitionA;

            // Edge cases: If partition is at boundary, use -infinity or +infinity
            int maxLeftA = (partitionA == 0) ? Integer.MIN_VALUE : nums1[partitionA - 1];
            int minRightA = (partitionA == m) ? Integer.MAX_VALUE : nums1[partitionA];

            int maxLeftB = (partitionB == 0) ? Integer.MIN_VALUE : nums2[partitionB - 1];
            int minRightB = (partitionB == n) ? Integer.MAX_VALUE : nums2[partitionB];

            if (maxLeftA <= minRightB && maxLeftB <= minRightA) {
                // Correct partition found
                if ((m + n) % 2 == 0) {
                    return ((double) Math.max(maxLeftA, maxLeftB) + Math.min(minRightA, minRightB)) / 2.0;
                } else {
                    return (double) Math.max(maxLeftA, maxLeftB);
                }
            } else if (maxLeftA > minRightB) {
                // Partition in A is too far right; move left
                high = partitionA - 1;
            } else {
                // Partition in A is too far left; move right
                low = partitionA + 1;
            }
        }

        throw new IllegalArgumentException("Input arrays are not sorted!");
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 4: Median of Two Sorted Arrays");
        System.out.println("=================================================");

        // Test 1: Odd total length
        int[] a1 = {1, 3};
        int[] b1 = {2};
        double med1 = findMedianSortedArrays(a1, b1);
        System.out.println("Test 1 [1,3] & [2] -> Expected 2.0: " + med1);
        assert Math.abs(med1 - 2.0) < 1e-6 : "Failed Test 1";

        // Test 2: Even total length
        int[] a2 = {1, 2};
        int[] b2 = {3, 4};
        double med2 = findMedianSortedArrays(a2, b2);
        System.out.println("Test 2 [1,2] & [3,4] -> Expected 2.5: " + med2);
        assert Math.abs(med2 - 2.5) < 1e-6 : "Failed Test 2";

        // Test 3: One empty array
        int[] a3 = {};
        int[] b3 = {1};
        double med3 = findMedianSortedArrays(a3, b3);
        System.out.println("Test 3 [] & [1] -> Expected 1.0: " + med3);
        assert Math.abs(med3 - 1.0) < 1e-6 : "Failed Test 3";

        // Test 4: Disjoint ranges
        int[] a4 = {1, 2, 3};
        int[] b4 = {4, 5, 6, 7};
        double med4 = findMedianSortedArrays(a4, b4);
        System.out.println("Test 4 [1,2,3] & [4,5,6,7] -> Expected 4.0: " + med4);
        assert Math.abs(med4 - 4.0) < 1e-6 : "Failed Test 4";

        System.out.println("\n✅ All Median of Two Sorted Arrays tests passed successfully!");
    }
}
