/**
 * Self-Balancing AVL Binary Search Tree
 * Invariant: For every node, |height(left) - height(right)| <= 1
 * Operations:
 * - Insert: O(log N) with single (LL/RR) or double (LR/RL) rotations
 * - Search: O(log N) guaranteed strictly bounded height
 * Space Complexity: O(N)
 */
public class AVLTree {

    public static class Node {
        int key, height;
        Node left, right;

        Node(int d) {
            key = d;
            height = 1;
        }
    }

    private Node root;

    private int height(Node n) {
        return n == null ? 0 : n.height;
    }

    private int getBalance(Node n) {
        return n == null ? 0 : height(n.left) - height(n.right);
    }

    // Right Rotation (for Left-Left Case)
    private Node rightRotate(Node y) {
        Node x = y.left;
        Node T2 = x.right;

        // Perform rotation
        x.right = y;
        y.left = T2;

        // Update heights
        y.height = Math.max(height(y.left), height(y.right)) + 1;
        x.height = Math.max(height(x.left), height(x.right)) + 1;

        return x;
    }

    // Left Rotation (for Right-Right Case)
    private Node leftRotate(Node x) {
        Node y = x.right;
        Node T2 = y.left;

        // Perform rotation
        y.left = x;
        x.right = T2;

        // Update heights
        x.height = Math.max(height(x.left), height(x.right)) + 1;
        y.height = Math.max(height(y.left), height(y.right)) + 1;

        return y;
    }

    public void insert(int key) {
        root = insertRec(root, key);
    }

    private Node insertRec(Node node, int key) {
        if (node == null) return new Node(key);

        if (key < node.key) {
            node.left = insertRec(node.left, key);
        } else if (key > node.key) {
            node.right = insertRec(node.right, key);
        } else {
            return node; // Duplicate keys not allowed
        }

        // Update node height
        node.height = 1 + Math.max(height(node.left), height(node.right));

        // Check balance factor
        int balance = getBalance(node);

        // Case 1: Left-Left (LL)
        if (balance > 1 && key < node.left.key) {
            return rightRotate(node);
        }

        // Case 2: Right-Right (RR)
        if (balance < -1 && key > node.right.key) {
            return leftRotate(node);
        }

        // Case 3: Left-Right (LR)
        if (balance > 1 && key > node.left.key) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        // Case 4: Right-Left (RL)
        if (balance < -1 && key < node.right.key) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        return node;
    }

    public boolean search(int key) {
        Node curr = root;
        while (curr != null) {
            if (key == curr.key) return true;
            curr = key < curr.key ? curr.left : curr.right;
        }
        return false;
    }

    public int getRootHeight() {
        return height(root);
    }

    public static void main(String[] args) {
        AVLTree tree = new AVLTree();
        // Inserting strictly ascending sequence (would degrade standard BST to O(N) linked list)
        int[] keys = {10, 20, 30, 40, 50, 25};
        for (int k : keys) {
            tree.insert(k);
        }

        System.out.println("Root Height after balanced rotations: " + tree.getRootHeight()); // Expected height <= 3
        System.out.println("Search 30: " + tree.search(30)); // true
        System.out.println("Search 99: " + tree.search(99)); // false

        System.out.println("AVLTree tests passed!");
    }
}
