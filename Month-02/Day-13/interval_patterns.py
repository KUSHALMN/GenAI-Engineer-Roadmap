"""
Interval & Sorting Patterns (Python).
Problems Implemented:
1. Merge Intervals (LC 56) - O(N log N) time, O(N) space
2. Insert Interval (LC 57) - O(N) time, O(N) space
3. Meeting Rooms (LC 252) - O(N log N) time, O(1) space
4. Meeting Rooms II (LC 253) - Min-Heap / Two Pointers, O(N log N) time, O(N) space
"""

import heapq
from typing import List


class IntervalPatterns:

    @staticmethod
    def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
        """LC 56: Merge overlapping intervals."""
        if not intervals:
            return []

        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]

        for current in intervals[1:]:
            prev = merged[-1]
            if current[0] <= prev[1]:
                # Overlap: extend previous interval's end
                prev[1] = max(prev[1], current[1])
            else:
                merged.append(current)

        return merged

    @staticmethod
    def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
        """LC 57: Insert Interval into non-overlapping sorted intervals."""
        result = []
        i = 0
        n = len(intervals)

        # 1. Add all intervals ending before new_interval begins
        while i < n and intervals[i][1] < new_interval[0]:
            result.append(intervals[i])
            i += 1

        # 2. Merge all overlapping intervals
        while i < n and intervals[i][0] <= new_interval[1]:
            new_interval[0] = min(new_interval[0], intervals[i][0])
            new_interval[1] = max(new_interval[1], intervals[i][1])
            i += 1
        result.append(new_interval)

        # 3. Add remaining intervals
        while i < n:
            result.append(intervals[i])
            i += 1

        return result

    @staticmethod
    def can_attend_meetings(intervals: List[List[int]]) -> bool:
        """LC 252: Meeting Rooms - Determine if person could attend all meetings."""
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True

    @staticmethod
    def min_meeting_rooms(intervals: List[List[int]]) -> int:
        """LC 253: Meeting Rooms II - Minimum conference rooms required."""
        if not intervals:
            return 0

        # Sort by start times
        intervals.sort(key=lambda x: x[0])

        # Min-heap to track earliest ending meetings
        rooms = []
        heapq.heappush(rooms, intervals[0][1])

        for meeting in intervals[1:]:
            start, end = meeting
            # If the earliest room is free before this meeting starts, reuse it
            if rooms[0] <= start:
                heapq.heappop(rooms)
            heapq.heappush(rooms, end)

        return len(rooms)


if __name__ == "__main__":
    ip = IntervalPatterns()

    # LC 56 Merge
    assert ip.merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert ip.merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]

    # LC 57 Insert
    assert ip.insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert ip.insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2], [3, 10], [12, 16]
    ]

    # LC 252 Meeting Rooms
    assert ip.can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
    assert ip.can_attend_meetings([[7, 10], [2, 4]]) is True

    # LC 253 Meeting Rooms II
    assert ip.min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert ip.min_meeting_rooms([[7, 10], [2, 4]]) == 1

    print("All Interval & Sorting Python tests passed successfully!")
