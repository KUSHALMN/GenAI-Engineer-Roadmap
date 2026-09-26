"""
Topological Sort for Directed Acyclic Graphs (DAGs) in Python.
Problems Implemented:
1. Course Schedule II (LC 210) - Kahn's Algorithm (BFS), O(V + E) time, O(V + E) space
2. Topological Sort via DFS (Cycle detection with White/Gray/Black states) - O(V + E) time
3. Task Dependency Resolver for Build/Workflow Systems
"""

from collections import defaultdict, deque
from typing import Dict, List, Optional


class TopologicalSort:

    @staticmethod
    def find_order_bfs(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        LC 210: Course Schedule II (Kahn's BFS Algorithm).
        Returns valid ordering if DAG, or empty list [] if cycle exists.
        """
        adj = defaultdict(list)
        in_degree = [0] * num_courses

        for dest, src in prerequisites:
            adj[src].append(dest)
            in_degree[dest] += 1

        queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == num_courses else []

    @staticmethod
    def find_order_dfs(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Topological Sort using DFS with 3-state cycle detection:
        0: Unvisited (White), 1: Visiting (Gray), 2: Visited (Black)
        """
        adj = defaultdict(list)
        for dest, src in prerequisites:
            adj[src].append(dest)

        state = [0] * num_courses
        order = []
        has_cycle = False

        def dfs(node: int):
            nonlocal has_cycle
            if has_cycle:
                return

            state[node] = 1  # visiting
            for neighbor in adj[node]:
                if state[neighbor] == 1:
                    has_cycle = True
                    return
                elif state[neighbor] == 0:
                    dfs(neighbor)

            state[node] = 2  # visited
            order.append(node)

        for i in range(num_courses):
            if state[i] == 0:
                dfs(i)

        if has_cycle:
            return []
        return order[::-1]  # reverse postorder

    @staticmethod
    def resolve_task_dependencies(tasks: Dict[str, List[str]]) -> List[str]:
        """
        Build system task resolver.
        Input: {task_name: [list_of_dependency_task_names]}
        """
        adj = defaultdict(list)
        in_degree = {task: 0 for task in tasks}

        for task, deps in tasks.items():
            for dep in deps:
                adj[dep].append(task)
                in_degree[task] += 1

        queue = deque([t for t, deg in in_degree.items() if deg == 0])
        resolved_order = []

        while queue:
            curr = queue.popleft()
            resolved_order.append(curr)

            for dependent in adj[curr]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(resolved_order) != len(tasks):
            raise ValueError("Circular dependency detected in tasks!")

        return resolved_order


if __name__ == "__main__":
    ts = TopologicalSort()

    # LC 210: 4 courses: [1,0], [2,0], [3,1], [3,2]
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order_bfs = ts.find_order_bfs(4, prereqs)
    print("Topological Order BFS:", order_bfs)
    assert order_bfs in ([0, 1, 2, 3], [0, 2, 1, 3])

    order_dfs = ts.find_order_dfs(4, prereqs)
    print("Topological Order DFS:", order_dfs)
    assert len(order_dfs) == 4

    # Cycle test: [1, 0], [0, 1]
    assert ts.find_order_bfs(2, [[1, 0], [0, 1]]) == []
    assert ts.find_order_dfs(2, [[1, 0], [0, 1]]) == []

    # Build system test
    build_tasks = {
        "compile": [],
        "test": ["compile"],
        "package": ["test"],
        "deploy": ["package"],
    }
    resolved = ts.resolve_task_dependencies(build_tasks)
    print("Resolved Tasks:", resolved)
    assert resolved == ["compile", "test", "package", "deploy"]

    print("All Topological Sort Python tests passed successfully!")
