import java.util.HashSet;
import java.util.ArrayList;

public class intersection_arrays {
    // LeetCode #349 - Intersection of Two Arrays
    // Approach: HashSet O(n)
    public int[] intersection(int[] nums1, int[] nums2) {
        HashSet<Integer> set = new HashSet<>();
        for (int n : nums1) set.add(n);

        ArrayList<Integer> result = new ArrayList<>();
        for (int n : nums2) {
            if (set.remove(n)) result.add(n);
        }

        return result.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        intersection_arrays sol = new intersection_arrays();
        int[] result = sol.intersection(new int[]{1, 2, 2, 1}, new int[]{2, 2});
        for (int n : result) System.out.print(n + " "); // 2
        System.out.println();

        result = sol.intersection(new int[]{4, 9, 5}, new int[]{9, 4, 9, 8, 4});
        for (int n : result) System.out.print(n + " "); // 9 4
    }
}
