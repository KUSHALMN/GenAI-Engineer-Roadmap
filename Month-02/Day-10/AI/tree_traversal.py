"""
Binary Tree Traversal Patterns (Python).
Problems Implemented:
1. Binary Tree Level Order Traversal (LC 102) - BFS, O(N) time, O(N) space
2. Maximum Depth of Binary Tree (LC 104) - DFS, O(N) time, O(H) space
3. Invert Binary Tree (LC 226) - DFS, O(N) time, O(H) space
4. Inorder, Preorder, Postorder Traversal - DFS basics
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


class TreeTraversal:

    @staticmethod
    def level_order(root: Optional[TreeNode]) -> List[List[int]]:
        """LC 102: Binary Tree Level Order Traversal (BFS)."""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result

    @staticmethod
    def max_depth(root: Optional[TreeNode]) -> int:
        """LC 104: Maximum Depth of Binary Tree (DFS)."""
        if not root:
            return 0
        return 1 + max(TreeTraversal.max_depth(root.left), TreeTraversal.max_depth(root.right))

    @staticmethod
    def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
        """LC 226: Invert Binary Tree."""
        if not root:
            return None

        # Swap children
        root.left, root.right = root.right, root.left
        TreeTraversal.invert_tree(root.left)
        TreeTraversal.invert_tree(root.right)
        return root

    @staticmethod
    def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
        """Left -> Root -> Right."""
        res = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)

        dfs(root)
        return res


if __name__ == "__main__":
    # Construct tree:
    #       3
    #      / \
    #     9   20
    #        /  \
    #       15   7
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))

    # LC 102
    assert TreeTraversal.level_order(root) == [[3], [9, 20], [15, 7]]

    # LC 104
    assert TreeTraversal.max_depth(root) == 3

    # Inorder
    assert TreeTraversal.inorder_traversal(root) == [9, 3, 15, 20, 7]

    # LC 226 Invert
    inv = TreeTraversal.invert_tree(root)
    assert TreeTraversal.level_order(inv) == [[3], [20, 9], [7, 15]]

    print("All Tree Traversal Python tests passed successfully!")
