import java.util.*;

/**
 * Problem: Top K Frequent Elements (LeetCode 347)
 * 
 * Approaches:
 * 1. HashMap + Min-Heap (PriorityQueue):
 *    - Count frequency of each number using a HashMap.
 *    - Maintain a Min-Heap of map entries/keys ordered by frequency ascending.
 *    - Heap size maintained <= K.
 *    - Time Complexity: O(N log K) where N is array length
 *    - Space Complexity: O(N + K)
 * 
 * 2. Bucket Sort (Linear Time O(N)):
 *    - Count frequencies using HashMap.
 *    - Create array of lists (buckets) where index represents frequency (0 to N).
 *    - Group numbers into buckets based on frequency.
 *    - Iterate buckets from end (highest frequency) downwards until K elements gathered.
 *    - Time Complexity: O(N)
 *    - Space Complexity: O(N)
 */
public class top_k_frequent {

    // Approach 1: Min-Heap
    public static int[] topKFrequentHeap(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) {
            return new int[0];
        }

        // Step 1: Count frequencies
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);
        }

        // Step 2: Min-Heap ordered by frequency
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(freqMap::get)
        );

        for (int num : freqMap.keySet()) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        // Step 3: Extract top k
        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) {
            result[i] = minHeap.poll();
        }

        return result;
    }

    // Approach 2: Bucket Sort (O(N) Time)
    public static int[] topKFrequentBucketSort(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) {
            return new int[0];
        }

        // Step 1: Frequency map
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);
        }

        // Step 2: Buckets indexed by frequency
        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new List[nums.length + 1];

        for (Map.Entry<Integer, Integer> entry : freqMap.entrySet()) {
            int freq = entry.getValue();
            if (buckets[freq] == null) {
                buckets[freq] = new ArrayList<>();
            }
            buckets[freq].add(entry.getKey());
        }

        // Step 3: Gather top k elements from highest frequency bucket down
        int[] result = new int[k];
        int idx = 0;

        for (int freq = buckets.length - 1; freq >= 0 && idx < k; freq--) {
            if (buckets[freq] != null) {
                for (int num : buckets[freq]) {
                    result[idx++] = num;
                    if (idx == k) {
                        break;
                    }
                }
            }
        }

        return result;
    }

    public static void main(String[] args) {
        System.out.println("=== Top K Frequent Elements ===");

        int[][] testCases = {
            {1, 1, 1, 2, 2, 3},
            {1},
            {4, 1, -1, 2, -1, 2, 3},
            {5, 3, 1, 1, 1, 3, 73, 1}
        };
        int[] kValues = {2, 1, 2, 2};

        for (int i = 0; i < testCases.length; i++) {
            int[] nums = testCases[i];
            int k = kValues[i];

            int[] heapRes = topKFrequentHeap(nums, k);
            int[] bucketRes = topKFrequentBucketSort(nums, k);

            System.out.println("\nTest Case " + (i + 1) + ":");
            System.out.println("Array: " + Arrays.toString(nums) + ", k = " + k);
            System.out.println("Heap Approach Result:        " + Arrays.toString(heapRes));
            System.out.println("Bucket Sort Approach Result: " + Arrays.toString(bucketRes));
        }

        System.out.println("\nAll test cases executed successfully!");
    }
}
