public class binary_search {
    // LeetCode #704 - Binary Search
    // Approach: Binary Search O(log n)
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        binary_search sol = new binary_search();
        System.out.println(sol.search(new int[]{-1, 0, 3, 5, 9, 12}, 9));  // 4
        System.out.println(sol.search(new int[]{-1, 0, 3, 5, 9, 12}, 2));  // -1
    }
}
