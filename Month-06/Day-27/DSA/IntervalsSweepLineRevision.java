import java.util.*;

public class IntervalsSweepLineRevision {
    // 1. LC 56: Merge Intervals
    public static int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        List<int[]> merged = new ArrayList<>();
        int[] curr = intervals[0];
        merged.add(curr);

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= curr[1]) {
                curr[1] = Math.max(curr[1], intervals[i][1]);
            } else {
                curr = intervals[i];
                merged.add(curr);
            }
        }
        return merged.toArray(new int[merged.size()][]);
    }

    // 2. LC 253: Meeting Rooms II (Min-Heap / Sweep Line)
    public static int minMeetingRooms(int[][] intervals) {
        if (intervals == null || intervals.length == 0) return 0;
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        PriorityQueue<Integer> endTimes = new PriorityQueue<>();
        endTimes.offer(intervals[0][1]);

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= endTimes.peek()) {
                endTimes.poll(); // Room freed
            }
            endTimes.offer(intervals[i][1]);
        }
        return endTimes.size();
    }

    public static void main(String[] args) {
        System.out.println("=== Intervals & Sweep Line Verification ===");
        int[][] intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
        int[][] res = merge(intervals);
        System.out.println("LC 56 (Merged): " + Arrays.deepToString(res));
        assert res.length == 3 && res[0][1] == 6 : "LC 56 failed";

        int[][] meetings = {{0, 30}, {5, 10}, {15, 20}};
        int rooms = minMeetingRooms(meetings);
        System.out.println("LC 253 (Min Rooms): " + rooms + " (Expected 2)");
        assert rooms == 2 : "LC 253 failed";
        System.out.println("Intervals passed!");
    }
}
