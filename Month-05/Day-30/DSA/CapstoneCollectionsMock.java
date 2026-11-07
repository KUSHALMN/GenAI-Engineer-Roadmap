import java.util.*;

/**
 * Day 30: DSA Mock Interview — Java Collections, Complexity & Concurrency
 * Problem 1: Top K Frequent Elements (Bucket Sort O(n))
 * Problem 2: Valid Parentheses Stack (O(n))
 */
public class CapstoneCollectionsMock {

    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);

        List<Integer>[] buckets = new List[nums.length + 1];
        for (int key : counts.keySet()) {
            int freq = counts.get(key);
            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
            buckets[freq].add(key);
        }

        int[] res = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null) {
                for (int val : buckets[i]) {
                    res[idx++] = val;
                    if (idx == k) break;
                }
            }
        }
        return res;
    }

    public boolean isValidParentheses(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        CapstoneCollectionsMock mock = new CapstoneCollectionsMock();
        int[] top2 = mock.topKFrequent(new int[]{1, 1, 1, 2, 2, 3}, 2);
        assert top2.length == 2;
        assert mock.isValidParentheses("({[]})");
        assert !mock.isValidParentheses("([)]");
        System.out.println("Day 30 DSA CapstoneCollectionsMock verification passed!");
    }
}
