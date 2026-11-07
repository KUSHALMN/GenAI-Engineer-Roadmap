import java.util.*;

/**
 * Day 04: PriorityQueue & Custom Comparators
 * Implements min-heap and max-heap scheduling, solving Top-K and deadline-based scheduling.
 *
 * Time Complexity: O(log k) per insertion into PriorityQueue.
 * Space Complexity: O(k)
 */
public class PriorityQueueScheduler {

    static class Job {
        String id;
        int priority; // Higher number = higher priority
        Job(String id, int priority) { this.id = id; this.priority = priority; }
    }

    public static void main(String[] args) {
        // Max-heap ordered by priority descending
        PriorityQueue<Job> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b.priority, a.priority));
        maxHeap.offer(new Job("J1", 10));
        maxHeap.offer(new Job("J2", 90));
        maxHeap.offer(new Job("J3", 50));

        assert maxHeap.poll().id.equals("J2") : "Highest priority job must be J2";
        assert maxHeap.poll().id.equals("J3") : "Next job must be J3";

        // Top K Frequent numbers using Min-Heap
        int[] nums = {1, 1, 1, 2, 2, 3};
        int k = 2;
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);

        PriorityQueue<Integer> minHeap = new PriorityQueue<>(Comparator.comparingInt(counts::get));
        for (int num : counts.keySet()) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }

        assert minHeap.contains(1) && minHeap.contains(2);
        System.out.println("Top-2 elements in min-heap: " + minHeap);
        System.out.println("Day 04 DSA PriorityQueueScheduler verification passed!");
    }
}
