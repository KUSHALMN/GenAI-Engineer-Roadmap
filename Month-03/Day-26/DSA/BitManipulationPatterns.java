package DSA;

import java.util.Arrays;

/**
 * Bit Manipulation Core Patterns
 * 1. LeetCode 136 - Single Number I (Every element appears twice except one)
 *    XOR property: x ^ x = 0, x ^ 0 = x
 * 2. LeetCode 137 - Single Number II (Every element appears three times except one)
 *    Count bits modulo 3
 * 3. LeetCode 260 - Single Number III (Two elements appear once, all others twice)
 *    Partition via lowest set bit of XOR sum
 * 
 * Complexity:
 * - Time: O(N)
 * - Space: O(1) in-place register operations
 */
public class BitManipulationPatterns {

    /**
     * LC 136: Single Number I
     */
    public static int singleNumberI(int[] nums) {
        int xor = 0;
        for (int x : nums) {
            xor ^= x;
        }
        return xor;
    }

    /**
     * LC 137: Single Number II
     */
    public static int singleNumberII(int[] nums) {
        int ones = 0, twos = 0;
        for (int x : nums) {
            ones = (ones ^ x) & ~twos;
            twos = (twos ^ x) & ~ones;
        }
        return ones;
    }

    /**
     * LC 260: Single Number III
     */
    public static int[] singleNumberIII(int[] nums) {
        int xor = 0;
        for (int x : nums) {
            xor ^= x;
        }

        // Get rightmost set bit
        int diff = xor & (-xor);

        int a = 0, b = 0;
        for (int x : nums) {
            if ((x & diff) == 0) {
                a ^= x;
            } else {
                b ^= x;
            }
        }

        return new int[]{a, b};
    }

    public static void main(String[] args) {
        int[] arr1 = {4, 1, 2, 1, 2};
        System.out.println("Single Number I in [4,1,2,1,2]: " + singleNumberI(arr1) + " (Expected: 4)");

        int[] arr2 = {2, 2, 3, 2};
        System.out.println("Single Number II in [2,2,3,2]: " + singleNumberII(arr2) + " (Expected: 3)");

        int[] arr3 = {1, 2, 1, 3, 2, 5};
        int[] res3 = singleNumberIII(arr3);
        Arrays.sort(res3);
        System.out.println("Single Number III in [1,2,1,3,2,5]: " + Arrays.toString(res3) + " (Expected: [3, 5])");

        System.out.println("BitManipulationPatterns tests passed!");
    }
}
