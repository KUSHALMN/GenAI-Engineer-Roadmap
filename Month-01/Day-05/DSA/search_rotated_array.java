public class search_rotated_array {
    // LeetCode #33 - Search in Rotated Sorted Array
    // Approach: Binary Search O(log n)
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;

            // Left half is sorted
            if (nums[left] <= nums[mid]) {
                if (nums[left] <= target && target < nums[mid]) right = mid - 1;
                else left = mid + 1;
            } else {
                // Right half is sorted
                if (nums[mid] < target && target <= nums[right]) left = mid + 1;
                else right = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        search_rotated_array sol = new search_rotated_array();
        System.out.println(sol.search(new int[]{4, 5, 6, 7, 0, 1, 2}, 0)); // 4
        System.out.println(sol.search(new int[]{4, 5, 6, 7, 0, 1, 2}, 3)); // -1
        System.out.println(sol.search(new int[]{1}, 0));                    // -1
    }
}
