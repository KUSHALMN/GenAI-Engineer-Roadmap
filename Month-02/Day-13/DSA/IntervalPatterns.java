import java.util.*;

/**
 * Interval & Sorting Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 56  - Merge Intervals -> O(N log N) time, O(N) space
 *   2. LeetCode 57  - Insert Interval -> O(N) time, O(N) space
 *   3. LeetCode 253 - Meeting Rooms II -> O(N log N) time, O(N) space
 */
public class IntervalPatterns {

    /**
     * LC 56: Merge Intervals
     */
    public int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;

        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        List<int[]> merged = new ArrayList<>();

        int[] currentInterval = intervals[0];
        merged.add(currentInterval);

        for (int[] interval : intervals) {
            int currentEnd = currentInterval[1];
            int nextBegin = interval[0];
            int nextEnd = interval[1];

            if (currentEnd >= nextBegin) {
                currentInterval[1] = Math.max(currentEnd, nextEnd);
            } else {
                currentInterval = interval;
                merged.add(currentInterval);
            }
        }

        return merged.toArray(new int[merged.size()][]);
    }

    /**
     * LC 57: Insert Interval
     */
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> result = new ArrayList<>();
        int i = 0;
        int n = intervals.length;

        // 1. Add all intervals ending before newInterval starts
        while (i < n && intervals[i][1] < newInterval[0]) {
            result.add(intervals[i]);
            i++;
        }

        // 2. Merge overlapping intervals
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.add(newInterval);

        // 3. Add remaining intervals
        while (i < n) {
            result.add(intervals[i]);
            i++;
        }

        return result.toArray(new int[result.size()][]);
    }

    /**
     * LC 253: Meeting Rooms II (Min-Heap)
     */
    public int minMeetingRooms(int[][] intervals) {
        if (intervals == null || intervals.length == 0) return 0;

        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        PriorityQueue<Integer> allocator = new PriorityQueue<>(
            intervals.length,
            Comparator.naturalOrder()
        );

        allocator.add(intervals[0][1]);

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= allocator.peek()) {
                allocator.poll();
            }
            allocator.add(intervals[i][1]);
        }

        return allocator.size();
    }

    public static void main(String[] args) {
        IntervalPatterns ip = new IntervalPatterns();

        // 1. Merge Intervals
        int[][] intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
        int[][] merged = ip.merge(intervals);
        System.out.println("LC 56 Merged: " + Arrays.deepToString(merged)); // [[1, 6], [8, 10], [15, 18]]

        // 2. Insert Interval
        int[][] inserted = ip.insert(new int[][]{{1, 3}, {6, 9}}, new int[]{2, 5});
        System.out.println("LC 57 Inserted: " + Arrays.deepToString(inserted)); // [[1, 5], [6, 9]]

        // 3. Meeting Rooms II
        int rooms = ip.minMeetingRooms(new int[][]{{0, 30}, {5, 10}, {15, 20}});
        System.out.println("LC 253 Min Meeting Rooms: " + rooms); // 2
    }
}
