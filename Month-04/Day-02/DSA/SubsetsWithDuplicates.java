import java.util.*;

/**
 * Day 02: Backtracking — Subsets II (Handling Duplicates)
 * Problem: Given an integer array nums that may contain duplicates, return all possible subsets (the power set).
 * The solution set must not contain duplicate subsets.
 *
 * Algorithm:
 * 1. Sort the input array to place identical elements adjacent.
 * 2. In the backtracking loop, if nums[i] == nums[i-1] and i > start, skip the iteration to avoid duplicate subtrees.
 *
 * Time Complexity: O(n * 2^n) where n = nums.length
 * Space Complexity: O(n) for recursion stack depth.
 */
public class SubsetsWithDuplicates {

    public List<List<Integer>> subsetsWithDup(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums); // Critical: sorting groups duplicates together
        backtrack(0, nums, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int start, int[] nums, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current));

        for (int i = start; i < nums.length; i++) {
            // Skip duplicates at the same tree depth level
            if (i > start && nums[i] == nums[i - 1]) {
                continue;
            }
            current.add(nums[i]);
            backtrack(i + 1, nums, current, result);
            current.remove(current.size() - 1); // backtrack
        }
    }

    public static void main(String[] args) {
        SubsetsWithDuplicates solver = new SubsetsWithDuplicates();
        int[] nums = {1, 2, 2};
        List<List<Integer>> subsets = solver.subsetsWithDup(nums);

        System.out.println("Subsets for {1, 2, 2} (No duplicates):");
        System.out.println(subsets);

        // Assertions
        assert subsets.size() == 6 : "Expected 6 unique subsets for [1, 2, 2]";
        System.out.println("Day 02 DSA SubsetsWithDuplicates verification passed!");
    }
}
