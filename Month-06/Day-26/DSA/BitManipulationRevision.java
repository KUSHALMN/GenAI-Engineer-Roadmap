public class BitManipulationRevision {
    // 1. LC 136: Single Number (XOR)
    public static int singleNumber(int[] nums) {
        int res = 0;
        for (int n : nums) res ^= n;
        return res;
    }

    // 2. LC 338: Counting Bits
    public static int[] countBits(int n) {
        int[] ans = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }

    // 3. LC 191: Number of 1 Bits (Brian Kernighan)
    public static int hammingWeight(int n) {
        int count = 0;
        while (n != 0) {
            n &= (n - 1);
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println("=== Bit Manipulation Verification ===");
        int[] nums = {4, 1, 2, 1, 2};
        int single = singleNumber(nums);
        System.out.println("LC 136 (Single Number in [4,1,2,1,2]): " + single + " (Expected 4)");
        assert single == 4 : "LC 136 failed";

        int[] bits = countBits(5);
        System.out.println("LC 338 (Counting Bits up to 5): " + java.util.Arrays.toString(bits));
        assert bits[5] == 2 : "LC 338 failed";
        System.out.println("Bit manipulation passed!");
    }
}
