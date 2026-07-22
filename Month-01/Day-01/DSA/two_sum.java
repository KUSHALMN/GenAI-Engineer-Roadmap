import java.util.HashMap;

public class two_sum {
    // LeetCode #1 - Two Sum
    // Approach: HashMap O(n)
    public int[] twoSum(int[] nums, int target) {
        HashMap<Integer, Integer> map = new HashMap<>();
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
        two_sum sol = new two_sum();
        int[] result = sol.twoSum(new int[]{2, 7, 11, 15}, 9);
        System.out.println("Output: [" + result[0] + ", " + result[1] + "]");
    }
}
