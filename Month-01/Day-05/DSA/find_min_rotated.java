public class find_min_rotated {
    // LeetCode #153 - Find Minimum in Rotated Sorted Array
    // Approach: Binary Search O(log n)
    public int findMin(int[] nums) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] > nums[right]) left = mid + 1;
            else right = mid;
        }
        return nums[left];
    }

    public static void main(String[] args) {
        find_min_rotated sol = new find_min_rotated();
        System.out.println(sol.findMin(new int[]{3, 4, 5, 1, 2})); // 1
        System.out.println(sol.findMin(new int[]{4, 5, 6, 7, 0, 1, 2})); // 0
        System.out.println(sol.findMin(new int[]{11, 13, 15, 17})); // 11
    }
}
