public class KnapsackRevision {
    // 1. LC 416: Partition Equal Subset Sum (0/1 Knapsack)
    public static boolean canPartition(int[] nums) {
        int sum = 0;
        for (int n : nums) sum += n;
        if (sum % 2 != 0) return false;
        int target = sum / 2;

        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : nums) {
            for (int j = target; j >= num; j--) {
                dp[j] = dp[j] || dp[j - num];
            }
        }
        return dp[target];
    }

    public static void main(String[] args) {
        System.out.println("=== Knapsack Patterns Verification ===");
        int[] nums1 = {1, 5, 11, 5};
        assert canPartition(nums1) : "LC 416 failed";
        System.out.println("LC 416 (Partition [1,5,11,5]): true (Expected true)");

        int[] nums2 = {1, 2, 3, 5};
        assert !canPartition(nums2) : "LC 416 failed";
        System.out.println("LC 416 (Partition [1,2,3,5]): false (Expected false)");
        System.out.println("Knapsack tests passed!");
    }
}
