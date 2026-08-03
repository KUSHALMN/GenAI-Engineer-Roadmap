public class search_insert_position {
    // LeetCode #35 - Search Insert Position
    // Approach: Binary Search O(log n)
    public int searchInsert(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return left;
    }

    public static void main(String[] args) {
        search_insert_position sol = new search_insert_position();
        System.out.println(sol.searchInsert(new int[]{1, 3, 5, 6}, 5)); // 2
        System.out.println(sol.searchInsert(new int[]{1, 3, 5, 6}, 2)); // 1
        System.out.println(sol.searchInsert(new int[]{1, 3, 5, 6}, 7)); // 4
    }
}
