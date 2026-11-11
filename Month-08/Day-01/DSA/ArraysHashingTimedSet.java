package Month08.Day01;

import java.util.HashMap;
import java.util.Map;

/**
 * Timed Set: Arrays and Hashing
 * LC 1: Two Sum - O(N) time and O(N) space.
 */
public class ArraysHashingTimedSet {

    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] indices = twoSum(nums, 9);
        assert indices.length == 2;
        assert indices[0] == 0 && indices[1] == 1;

        System.out.println("Day 01 Arrays and Hashing Timed Set verification passed.");
    }
}
