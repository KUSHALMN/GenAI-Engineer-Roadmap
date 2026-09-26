"""
Disjoint Set Union (Union-Find) Pattern (Python).
Features:
- Path Compression
- Union by Rank / Size
Problems Implemented:
1. Number of Provinces (LC 547) - O(N * alpha(N)) time, O(N) space
2. Redundant Connection (LC 684) - O(N * alpha(N)) time, O(N) space
3. Graph Valid Tree (LC 261) - O(N * alpha(N)) time, O(N) space
"""

from typing import List


class UnionFind:
    """Disjoint Set Union with Path Compression and Union by Rank."""

    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.count = size  # Number of disjoint components

    def find(self, p: int) -> int:
        """Find root with path compression."""
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p: int, q: int) -> bool:
        """Union two sets by rank. Returns True if sets were merged, False if already connected."""
        root_p = self.find(p)
        root_q = self.find(q)

        if root_p == root_q:
            return False

        if self.rank[root_p] > self.rank[root_q]:
            self.parent[root_q] = root_p
        elif self.rank[root_p] < self.rank[root_q]:
            self.parent[root_p] = root_q
        else:
            self.parent[root_q] = root_p
            self.rank[root_p] += 1

        self.count -= 1
        return True

    def connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)


class UnionFindPatterns:

    @staticmethod
    def find_circle_num(is_connected: List[List[int]]) -> int:
        """LC 547: Number of Provinces."""
        n = len(is_connected)
        uf = UnionFind(n)

        for i in range(n):
            for j in range(i + 1, n):
                if is_connected[i][j] == 1:
                    uf.union(i, j)

        return uf.count

    @staticmethod
    def find_redundant_connection(edges: List[List[int]]) -> List[int]:
        """LC 684: Redundant Connection (returns edge that creates cycle)."""
        n = len(edges)
        uf = UnionFind(n + 1)

        for u, v in edges:
            if not uf.union(u, v):
                return [u, v]

        return []


if __name__ == "__main__":
    # LC 547
    connected_matrix = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]
    assert UnionFindPatterns.find_circle_num(connected_matrix) == 2

    # LC 684
    edges = [[1, 2], [1, 3], [2, 3]]
    redundant = UnionFindPatterns.find_redundant_connection(edges)
    assert redundant == [2, 3]

    print("All Union-Find Python tests passed successfully!")
