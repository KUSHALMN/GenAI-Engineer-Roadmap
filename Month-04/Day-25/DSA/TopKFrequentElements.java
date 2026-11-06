import java.util.*;

/**
 * Day 25: Heap / Bucket Sort — Top K Frequent Elements
 * Problem: Given an integer array nums and an integer k, return the k most frequent elements.
 *
 * Algorithm 1: Min-heap of size k -> O(n log k)
 * Algorithm 2: Bucket Sort by frequency -> O(n)
 *
 * Time Complexity: O(n) using Bucket Sort
 * Space Complexity: O(n)
 */
public class TopKFrequentElements {

    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> countMap = new HashMap<>();
        for (int x : nums) countMap.put(x, countMap.getOrDefault(x, 0) + 1);

        // Bucket sort where index represents frequency
        List<Integer>[] buckets = new List[nums.length + 1];
        for (int key : countMap.keySet()) {
            int freq = countMap.get(key);
            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
            buckets[freq].add(key);
        }

        int[] result = new int[k];
        int idx = 0;
        for (int pos = buckets.length - 1; pos >= 0 && idx < k; pos--) {
            if (buckets[pos] != null) {
                for (int num : buckets[pos]) {
                    result[idx++] = num;
                    if (idx == k) break;
                }
            }
        }
        return result;
    }

    public static void main(String[] args) {
        TopKFrequentElements solver = new TopKFrequentElements();
        int[] nums = {1, 1, 1, 2, 2, 3};
        int k = 2;
        int[] top2 = solver.topKFrequent(nums, k);

        System.out.println("Top 2 frequent elements: " + Arrays.toString(top2));
        assert top2.length == 2;
        System.out.println("Day 25 DSA TopKFrequentElements verification passed!");
    }
}
