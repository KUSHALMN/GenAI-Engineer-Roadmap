import java.util.*;

/**
 * Day 04: Backtracking — Combination Sum
 * Problem: Given an array of distinct integers candidates and a target integer target,
 * return a list of all unique combinations where the chosen numbers sum to target.
 * The same number may be chosen unlimited times.
 *
 * Time Complexity: O(2^t) where t is target value
 * Space Complexity: O(t / min_candidate) recursion depth.
 */
public class CombinationSum {

    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(candidates);
        backtrack(0, candidates, target, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int start, int[] candidates, int remain, List<Integer> current, List<List<Integer>> result) {
        if (remain == 0) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > remain) break; // Prune search branch

            current.add(candidates[i]);
            // Notice: pass i (not i + 1) because reuse is permitted
            backtrack(i, candidates, remain - candidates[i], current, result);
            current.remove(current.size() - 1); // backtrack
        }
    }

    public static void main(String[] args) {
        CombinationSum solver = new CombinationSum();
        int[] candidates = {2, 3, 6, 7};
        int target = 7;
        List<List<Integer>> combinations = solver.combinationSum(candidates, target);

        System.out.println("Combinations summing to " + target + ": " + combinations);
        assert combinations.size() == 2 : "Expected 2 solutions: [2,2,3] and [7]";
        System.out.println("Day 04 DSA CombinationSum verification passed!");
    }
}
