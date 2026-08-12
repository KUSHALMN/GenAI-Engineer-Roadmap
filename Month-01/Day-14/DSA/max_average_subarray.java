public class max_average_subarray {
    // LeetCode #643 - Maximum Average Subarray I
    // Approach: Fixed sliding window O(n)
    public double findMaxAverage(int[] nums, int k) {
        double sum = 0;
        for (int i = 0; i < k; i++) sum += nums[i];
        double maxSum = sum;
        for (int i = k; i < nums.length; i++) {
            sum += nums[i] - nums[i - k];
            maxSum = Math.max(maxSum, sum);
        }
        return maxSum / k;
    }

    public static void main(String[] args) {
        max_average_subarray sol = new max_average_subarray();
        System.out.println(sol.findMaxAverage(new int[]{1,12,-5,-6,50,3}, 4));  // 12.75
        System.out.println(sol.findMaxAverage(new int[]{5}, 1));                 // 5.0
    }
}
