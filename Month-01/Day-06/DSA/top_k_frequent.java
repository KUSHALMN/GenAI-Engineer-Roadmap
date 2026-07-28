import java.util.HashMap;
import java.util.PriorityQueue;

public class top_k_frequent {
    // LeetCode #347 - Top K Frequent Elements
    // Approach: HashMap + Min-Heap O(n log k)
    public int[] topKFrequent(int[] nums, int k) {
        HashMap<Integer, Integer> freq = new HashMap<>();
        for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);

        PriorityQueue<Integer> heap = new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
        for (int n : freq.keySet()) {
            heap.offer(n);
            if (heap.size() > k) heap.poll();
        }

        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) result[i] = heap.poll();
        return result;
    }

    public static void main(String[] args) {
        top_k_frequent sol = new top_k_frequent();
        int[] result = sol.topKFrequent(new int[]{1, 1, 1, 2, 2, 3}, 2);
        for (int n : result) System.out.print(n + " "); // 1 2
        System.out.println();

        result = sol.topKFrequent(new int[]{1}, 1);
        for (int n : result) System.out.print(n + " "); // 1
    }
}
