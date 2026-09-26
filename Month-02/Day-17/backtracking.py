"""
Backtracking Patterns (Python).
Problems Implemented:
1. Subsets (LC 78) - O(2^N) time, O(N) space
2. Permutations (LC 46) - O(N! * N) time, O(N) space
3. Combinations (LC 77) - O(C(N, K)) time, O(K) space
4. Word Search (LC 79) - O(M * N * 3^L) time
5. N-Queens (LC 51) - O(N!) time, O(N) space
"""

from typing import List


class BacktrackingPatterns:

    @staticmethod
    def subsets(nums: List[int]) -> List[List[int]]:
        """LC 78: Subsets (Power Set)."""
        res = []

        def backtrack(start: int, current: List[int]):
            res.append(list(current))
            for i in range(start, len(nums)):
                current.append(nums[i])
                backtrack(i + 1, current)
                current.pop()

        backtrack(0, [])
        return res

    @staticmethod
    def permute(nums: List[int]) -> List[List[int]]:
        """LC 46: Permutations."""
        res = []
        used = [False] * len(nums)

        def backtrack(current: List[int]):
            if len(current) == len(nums):
                res.append(list(current))
                return

            for i in range(len(nums)):
                if not used[i]:
                    used[i] = True
                    current.append(nums[i])
                    backtrack(current)
                    current.pop()
                    used[i] = False

        backtrack([])
        return res

    @staticmethod
    def combine(n: int, k: int) -> List[List[int]]:
        """LC 77: Combinations (k numbers out of 1..n)."""
        res = []

        def backtrack(start: int, current: List[int]):
            if len(current) == k:
                res.append(list(current))
                return

            for i in range(start, n + 1):
                current.append(i)
                backtrack(i + 1, current)
                current.pop()

        backtrack(1, [])
        return res

    @staticmethod
    def exist(board: List[List[str]], word: str) -> bool:
        """LC 79: Word Search on 2D Board."""
        rows, cols = len(board), len(board[0])

        def backtrack(r: int, c: int, idx: int) -> bool:
            if idx == len(word):
                return True
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
                return False

            temp = board[r][c]
            board[r][c] = "#"  # mark visited

            found = (
                backtrack(r + 1, c, idx + 1)
                or backtrack(r - 1, c, idx + 1)
                or backtrack(r, c + 1, idx + 1)
                or backtrack(r, c - 1, idx + 1)
            )

            board[r][c] = temp  # unmark
            return found

        for r in range(rows):
            for c in range(cols):
                if backtrack(r, c, 0):
                    return True
        return False

    @staticmethod
    def solve_n_queens(n: int) -> List[List[str]]:
        """LC 51: N-Queens problem."""
        res = []
        cols = set()
        pos_diag = set()  # (r + c)
        neg_diag = set()  # (r - c)
        board = [["."] * n for _ in range(n)]

        def backtrack(r: int):
            if r == n:
                res.append(["".join(row) for row in board])
                return

            for c in range(n):
                if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                    continue

                cols.add(c)
                pos_diag.add(r + c)
                neg_diag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                cols.remove(c)
                pos_diag.remove(r + c)
                neg_diag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res


if __name__ == "__main__":
    bp = BacktrackingPatterns()

    # LC 78 Subsets
    subs = bp.subsets([1, 2, 3])
    assert len(subs) == 8

    # LC 46 Permutations
    perms = bp.permute([1, 2, 3])
    assert len(perms) == 6

    # LC 77 Combinations
    combs = bp.combine(4, 2)
    assert len(combs) == 6

    # LC 79 Word Search
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    assert bp.exist(board, "ABCCED") is True
    assert bp.exist(board, "SEE") is True
    assert bp.exist(board, "ABCB") is False

    # LC 51 N-Queens
    n4 = bp.solve_n_queens(4)
    assert len(n4) == 2

    print("All Backtracking Python tests passed successfully!")
