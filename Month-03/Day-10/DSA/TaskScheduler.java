import java.util.*;

/**
 * Task Scheduling & Greedy Heap Optimization
 * 1. LeetCode 621 - Task Scheduler: Minimum CPU intervals to run tasks with n cooldown
 *    Time Complexity: O(N), Space Complexity: O(1) for alphabet array.
 * 2. LeetCode 767 - Reorganize String: Rearrange characters so no two adjacent are identical
 *    Time Complexity: O(N log K) where K <= 26, Space: O(K).
 */
public class TaskScheduler {

    /**
     * LC 621: Task Scheduler
     * Uses frequency counting and idle slot greedy calculation.
     */
    public static int leastInterval(char[] tasks, int n) {
        int[] freq = new int[26];
        int maxFreq = 0;
        for (char c : tasks) {
            freq[c - 'A']++;
            maxFreq = Math.max(maxFreq, freq[c - 'A']);
        }

        int maxFreqCount = 0;
        for (int f : freq) {
            if (f == maxFreq) {
                maxFreqCount++;
            }
        }

        int partCount = maxFreq - 1;
        int partLength = n - (maxFreqCount - 1);
        int emptySlots = partCount * partLength;
        int availableTasks = tasks.length - (maxFreq * maxFreqCount);
        int idles = Math.max(0, emptySlots - availableTasks);

        return tasks.length + idles;
    }

    /**
     * LC 767: Reorganize String using Max-Heap
     */
    public static String reorganizeString(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : s.toCharArray()) {
            counts.put(c, counts.getOrDefault(c, 0) + 1);
        }

        PriorityQueue<Character> maxHeap = new PriorityQueue<>(
            (a, b) -> counts.get(b) - counts.get(a)
        );
        maxHeap.addAll(counts.keySet());

        StringBuilder sb = new StringBuilder();
        while (maxHeap.size() >= 2) {
            char first = maxHeap.poll();
            char second = maxHeap.poll();

            sb.append(first);
            sb.append(second);

            counts.put(first, counts.get(first) - 1);
            counts.put(second, counts.get(second) - 1);

            if (counts.get(first) > 0) maxHeap.offer(first);
            if (counts.get(second) > 0) maxHeap.offer(second);
        }

        if (!maxHeap.isEmpty()) {
            char last = maxHeap.poll();
            if (counts.get(last) > 1) {
                return ""; // Impossible to reorganize
            }
            sb.append(last);
        }

        return sb.toString();
    }

    public static void main(String[] args) {
        char[] tasks = {'A', 'A', 'A', 'B', 'B', 'B'};
        int cooldown = 2;
        int totalIntervals = leastInterval(tasks, cooldown);
        System.out.println("Least intervals for ['A','A','A','B','B','B'] with n=2: " + totalIntervals); // Expected 8

        String testStr = "aab";
        System.out.println("Reorganize 'aab': " + reorganizeString(testStr)); // "aba"

        String impossibleStr = "aaab";
        System.out.println("Reorganize 'aaab': '" + reorganizeString(impossibleStr) + "' (expected empty string)");

        System.out.println("TaskScheduler tests passed!");
    }
}
