"""
Graph BFS, DFS, Connected Components & Cycle Detection (Python).
Problems Implemented:
1. Number of Islands (LC 200) - BFS/DFS, O(M * N) time, O(M * N) space
2. Course Schedule / Cycle Detection in Directed Graph (LC 207) - Kahn's Algorithm / DFS, O(V + E) time
3. Clone Graph (LC 133) - BFS/DFS with Hash Map, O(V + E) time
4. Number of Connected Components in an Undirected Graph (LC 323) - DFS/Union-Find, O(V + E) time
"""

from collections import deque
from typing import Dict, List, Optional


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class GraphAlgorithms:

    @staticmethod
    def num_islands(grid: List[List[str]]) -> int:
        """LC 200: Number of Islands (DFS)."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        count = 0

        def dfs(r: int, c: int):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
                return
            grid[r][c] = "0"  # mark visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    dfs(r, c)

        return count

    @staticmethod
    def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
        """
        LC 207: Course Schedule (Cycle detection via Kahn's Algorithm - BFS).
        Returns True if all courses can be finished (DAG), False if cycle exists.
        """
        adj = [[] for _ in range(num_courses)]
        in_degree = [0] * num_courses

        for dest, src in prerequisites:
            adj[src].append(dest)
            in_degree[dest] += 1

        queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
        visited_count = 0

        while queue:
            node = queue.popleft()
            visited_count += 1

            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count == num_courses

    @staticmethod
    def clone_graph(node: Optional[Node]) -> Optional[Node]:
        """LC 133: Clone Graph (DFS with visited dictionary)."""
        if not node:
            return None

        clones: Dict[Node, Node] = {}

        def dfs(curr: Node) -> Node:
            if curr in clones:
                return clones[curr]

            copy = Node(curr.val)
            clones[curr] = copy

            for neighbor in curr.neighbors:
                copy.neighbors.append(dfs(neighbor))

            return copy

        return dfs(node)

    @staticmethod
    def count_components(n: int, edges: List[List[int]]) -> int:
        """LC 323: Number of Connected Components in an Undirected Graph."""
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()
        components = 0

        def dfs(node: int):
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        for i in range(n):
            if i not in visited:
                components += 1
                dfs(i)

        return components


if __name__ == "__main__":
    ga = GraphAlgorithms()

    # LC 200
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert ga.num_islands(grid) == 1

    # LC 207 (No cycle)
    assert ga.can_finish(2, [[1, 0]]) is True
    # LC 207 (Cycle: 0->1 and 1->0)
    assert ga.can_finish(2, [[1, 0], [0, 1]]) is False

    # LC 323
    assert ga.count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2

    print("All Graph BFS/DFS Python tests passed successfully!")
