import java.util.*;

/**
 * Day 01: Recursion Templates & Subsets
 * Problem: Given an integer array nums of unique elements, return all possible subsets (the power set).
 *
 * Algorithm:
 * - Decision Tree Backtracking: At each index, branch into two decisions:
 *   1) Include nums[index] in current subset
 *   2) Exclude nums[index] from current subset
 *
 * Time Complexity: O(n * 2^n) where n is nums.length (2^n subsets, each takes O(n) to copy)
 * Space Complexity: O(n) auxiliary recursion stack space.
 */
public class SubsetsRecursion {

    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int start, int[] nums, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current)); // Capture state at current node

        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);                  // Choose
            backtrack(i + 1, nums, current, result); // Explore
            current.remove(current.size() - 1);    // Un-choose (backtrack)
        }
    }

    public static void main(String[] args) {
        SubsetsRecursion solver = new SubsetsRecursion();
        int[] nums = {1, 2, 3};
        List<List<Integer>> subsets = solver.subsets(nums);

        System.out.println("Generated " + subsets.size() + " subsets for {1, 2, 3}:");
        System.out.println(subsets);

        // Verification assertions
        assert subsets.size() == 8 : "Expected 8 subsets for 3 elements";
        assert subsets.contains(Arrays.asList(1, 2, 3)) : "Missing full set";
        assert subsets.contains(Collections.emptyList()) : "Missing empty set";
        System.out.println("Day 01 DSA Subsets verification passed!");
    }
}
