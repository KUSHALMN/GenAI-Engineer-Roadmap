import java.util.*;

/**
 * Day 08: Bitmask Enumeration — Subsets
 * Problem: Generate all subsets using binary bitmask iteration.
 *
 * Algorithm:
 * - A set of size n has 2^n subsets, corresponding to numbers from 0 to (2^n - 1).
 * - If the j-th bit of number i is 1, include nums[j].
 *
 * Time Complexity: O(n * 2^n)
 * Space Complexity: O(1) auxiliary (excluding output).
 */
public class BitmaskSubsets {

    public List<List<Integer>> subsets(int[] nums) {
        int n = nums.length;
        int totalSubsets = 1 << n; // 2^n
        List<List<Integer>> result = new ArrayList<>();

        for (int mask = 0; mask < totalSubsets; mask++) {
            List<Integer> subset = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((mask & (1 << j)) != 0) {
                    subset.add(nums[j]);
                }
            }
            result.add(subset);
        }
        return result;
    }

    public static void main(String[] args) {
        BitmaskSubsets solver = new BitmaskSubsets();
        int[] nums = {4, 5, 6};
        List<List<Integer>> subsets = solver.subsets(nums);

        System.out.println("Bitmask generated " + subsets.size() + " subsets for [4, 5, 6]:");
        System.out.println(subsets);

        assert subsets.size() == 8;
        System.out.println("Day 08 DSA BitmaskSubsets verification passed!");
    }
}
