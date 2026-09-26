"""
Binary Search Tree (BST) Patterns (Python).
Problems Implemented:
1. Search in a Binary Search Tree (LC 700) - O(H) time, O(H) space
2. Insert into a Binary Search Tree (LC 701) - O(H) time, O(H) space
3. Delete Node in a BST (LC 450) - O(H) time, O(H) space
4. Validate Binary Search Tree (LC 98) - O(N) time, O(H) space
5. Lowest Common Ancestor of a BST (LC 235) - O(H) time, O(1) space
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


class BinarySearchTree:

    @staticmethod
    def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """LC 700: Search in BST."""
        curr = root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return None

    @staticmethod
    def insert_into_bst(root: Optional[TreeNode], val: int) -> TreeNode:
        """LC 701: Insert into BST."""
        if not root:
            return TreeNode(val)

        if val < root.val:
            root.left = BinarySearchTree.insert_into_bst(root.left, val)
        else:
            root.right = BinarySearchTree.insert_into_bst(root.right, val)

        return root

    @staticmethod
    def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """LC 450: Delete Node in a BST."""
        if not root:
            return None

        if key < root.val:
            root.left = BinarySearchTree.delete_node(root.left, key)
        elif key > root.val:
            root.right = BinarySearchTree.delete_node(root.right, key)
        else:
            # Case 1 & 2: 0 or 1 child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Case 3: 2 children - find inorder successor (min in right subtree)
            successor = root.right
            while successor.left:
                successor = successor.left

            root.val = successor.val
            root.right = BinarySearchTree.delete_node(root.right, successor.val)

        return root

    @staticmethod
    def is_valid_bst(root: Optional[TreeNode]) -> bool:
        """LC 98: Validate Binary Search Tree."""
        def validate(node, low=float("-inf"), high=float("inf")):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)

        return validate(root)

    @staticmethod
    def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """LC 235: Lowest Common Ancestor of a BST."""
        curr = root
        while curr:
            if p.val > curr.val and q.val > curr.val:
                curr = curr.right
            elif p.val < curr.val and q.val < curr.val:
                curr = curr.left
            else:
                return curr
        return root


if __name__ == "__main__":
    bst = BinarySearchTree()

    # Build BST:
    #       6
    #      / \
    #     2   8
    #    / \
    #   0   4
    root = TreeNode(6)
    root = bst.insert_into_bst(root, 2)
    root = bst.insert_into_bst(root, 8)
    root = bst.insert_into_bst(root, 0)
    root = bst.insert_into_bst(root, 4)

    # Validate
    assert bst.is_valid_bst(root) is True

    # Search
    found = bst.search_bst(root, 4)
    assert found is not None and found.val == 4

    # LCA
    node_0 = bst.search_bst(root, 0)
    node_4 = bst.search_bst(root, 4)
    lca = bst.lowest_common_ancestor(root, node_0, node_4)
    assert lca.val == 2

    # Delete
    root = bst.delete_node(root, 2)
    assert bst.search_bst(root, 2) is None
    assert bst.is_valid_bst(root) is True

    print("All BST Python tests passed successfully!")
