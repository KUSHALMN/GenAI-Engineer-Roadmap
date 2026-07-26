public class peak_index_mountain {
    // LeetCode #852 - Peak Index in a Mountain Array
    // Approach: Binary Search O(log n)
    public int peakIndexInMountainArray(int[] arr) {
        int left = 0, right = arr.length - 1;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] < arr[mid + 1]) left = mid + 1;
            else right = mid;
        }
        return left;
    }

    public static void main(String[] args) {
        peak_index_mountain sol = new peak_index_mountain();
        System.out.println(sol.peakIndexInMountainArray(new int[]{0, 1, 0}));       // 1
        System.out.println(sol.peakIndexInMountainArray(new int[]{0, 2, 1, 0}));    // 1
        System.out.println(sol.peakIndexInMountainArray(new int[]{0, 10, 5, 2}));   // 1
    }
}
