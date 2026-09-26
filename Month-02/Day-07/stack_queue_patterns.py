"""
Stack, Queue, Deque & Monotonic Stack Patterns (Python).
Problems Implemented:
1. Valid Parentheses (LC 20) - O(N) time, O(N) space
2. Daily Temperatures (LC 739) - Monotonic Decreasing Stack, O(N) time, O(N) space
3. Min Stack (LC 155) - O(1) time getMin, push, pop, top
4. Implement Queue using Stacks (LC 232) - Amortized O(1) time
"""

from typing import List


class StackQueuePatterns:

    @staticmethod
    def is_valid_parentheses(s: str) -> bool:
        """LC 20: Valid Parentheses."""
        mapping = {")": "(", "}": "{", "]": "["}
        stack = []

        for ch in s:
            if ch in mapping:
                top = stack.pop() if stack else "#"
                if mapping[ch] != top:
                    return False
            else:
                stack.append(ch)

        return not stack

    @staticmethod
    def daily_temperatures(temperatures: List[int]) -> List[int]:
        """
        LC 739: Daily Temperatures.
        Monotonic Decreasing Stack storing indices.
        """
        n = len(temperatures)
        ans = [0] * n
        stack = []  # indices of temps in decreasing order

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_idx = stack.pop()
                ans[prev_idx] = i - prev_idx
            stack.append(i)

        return ans


class MinStack:
    """
    LC 155: Min Stack.
    Maintains a parallel min stack or value/min tuples.
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]


class MyQueue:
    """
    LC 232: Implement Queue using Stacks (Two Stacks).
    """

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _transfer(self) -> None:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack


if __name__ == "__main__":
    sq = StackQueuePatterns()

    # LC 20
    assert sq.is_valid_parentheses("()[]{}") is True
    assert sq.is_valid_parentheses("(]") is False
    assert sq.is_valid_parentheses("([)]") is False

    # LC 739
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    expected = [1, 1, 4, 2, 1, 1, 0, 0]
    assert sq.daily_temperatures(temps) == expected

    # LC 155
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    assert min_stack.get_min() == -3
    min_stack.pop()
    assert min_stack.top() == 0
    assert min_stack.get_min() == -2

    # LC 232
    q = MyQueue()
    q.push(1)
    q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    assert q.empty() is False

    print("All Stack/Queue/Monotonic Python tests passed successfully!")
