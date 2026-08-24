import java.util.*;

/**
 * Problem: Clone Graph (LeetCode 133)
 * 
 * Given a reference of a node in a connected undirected graph.
 * Return a deep copy (clone) of the graph.
 * Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
 * 
 * Fundamental Concept:
 * - Graph Deep Copy with Reference Isolation.
 * - Using HashMap<Node, Node> to map original node pointers to newly instantiated cloned nodes.
 * - Prevents infinite recursion / queue loops in cyclic graphs.
 * 
 * Approaches:
 * 1. Depth-First Search (DFS) - Recursive:
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V) for visited map + recursion call stack.
 * 
 * 2. Breadth-First Search (BFS) - Iterative:
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V) for visited map + queue.
 */
public class clone_graph {

    // Node Definition
    public static class Node {
        public int val;
        public List<Node> neighbors;

        public Node() {
            this.val = 0;
            this.neighbors = new ArrayList<>();
        }

        public Node(int _val) {
            this.val = _val;
            this.neighbors = new ArrayList<>();
        }

        public Node(int _val, ArrayList<Node> _neighbors) {
            this.val = _val;
            this.neighbors = _neighbors;
        }
    }

    // ==========================================
    // Approach 1: Depth-First Search (DFS)
    // ==========================================
    public static Node cloneGraphDFS(Node node) {
        if (node == null) {
            return null;
        }
        Map<Node, Node> visited = new HashMap<>();
        return dfsHelper(node, visited);
    }

    private static Node dfsHelper(Node node, Map<Node, Node> visited) {
        if (visited.containsKey(node)) {
            return visited.get(node);
        }

        // Clone current node
        Node clone = new Node(node.val);
        visited.put(node, clone);

        // Recursively clone all neighbors
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(dfsHelper(neighbor, visited));
        }

        return clone;
    }

    // ==========================================
    // Approach 2: Breadth-First Search (BFS)
    // ==========================================
    public static Node cloneGraphBFS(Node node) {
        if (node == null) {
            return null;
        }

        Map<Node, Node> visited = new HashMap<>();
        Queue<Node> queue = new LinkedList<>();

        // Create root clone
        Node rootClone = new Node(node.val);
        visited.put(node, rootClone);
        queue.offer(node);

        while (!queue.isEmpty()) {
            Node curr = queue.poll();

            for (Node neighbor : curr.neighbors) {
                if (!visited.containsKey(neighbor)) {
                    visited.put(neighbor, new Node(neighbor.val));
                    queue.offer(neighbor);
                }
                visited.get(curr).neighbors.add(visited.get(neighbor));
            }
        }

        return rootClone;
    }

    // ==========================================
    // Graph Verification Helpers
    // ==========================================
    public static Node buildGraphFromAdjList(int[][] adjList) {
        if (adjList == null || adjList.length == 0) {
            return null;
        }

        int n = adjList.length;
        Node[] nodes = new Node[n + 1];
        for (int i = 1; i <= n; i++) {
            nodes[i] = new Node(i);
        }

        for (int i = 0; i < n; i++) {
            Node curr = nodes[i + 1];
            for (int neighborVal : adjList[i]) {
                curr.neighbors.add(nodes[neighborVal]);
            }
        }

        return nodes[1];
    }

    public static boolean verifyDeepCopy(Node original, Node clone) {
        if (original == null && clone == null) return true;
        if (original == null || clone == null) return false;

        Map<Node, Node> visited = new HashMap<>();
        Queue<Node[]> queue = new LinkedList<>();

        queue.offer(new Node[]{original, clone});
        visited.put(original, clone);

        while (!queue.isEmpty()) {
            Node[] pair = queue.poll();
            Node o = pair[0];
            Node c = pair[1];

            // 1. Same value check
            if (o.val != c.val) return false;
            // 2. Deep memory reference isolation check (must NOT share memory)
            if (o == c) return false;
            // 3. Same neighbor count check
            if (o.neighbors.size() != c.neighbors.size()) return false;

            for (int i = 0; i < o.neighbors.size(); i++) {
                Node oNeighbor = o.neighbors.get(i);
                Node cNeighbor = c.neighbors.get(i);

                if (visited.containsKey(oNeighbor)) {
                    if (visited.get(oNeighbor) != cNeighbor) return false;
                } else {
                    visited.put(oNeighbor, cNeighbor);
                    queue.offer(new Node[]{oNeighbor, cNeighbor});
                }
            }
        }
        return true;
    }

    // ==========================================
    // Test Suite and Main Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("      LeetCode 133: Clone Graph Test Suite       ");
        System.out.println("=================================================\n");

        // Test 1: 4-Node Cyclic Graph [[2,4],[1,3],[2,4],[1,3]]
        int[][] adj1 = {
            {2, 4}, // Node 1
            {1, 3}, // Node 2
            {2, 4}, // Node 3
            {1, 3}  // Node 4
        };
        Node g1 = buildGraphFromAdjList(adj1);
        testClone("Test 1: 4-Node Cyclic Graph", g1);

        // Test 2: Single isolated node [[]]
        int[][] adj2 = {{}};
        Node g2 = buildGraphFromAdjList(adj2);
        testClone("Test 2: Single Isolated Node", g2);

        // Test 3: Null / Empty graph []
        testClone("Test 3: Null Empty Graph", null);

        // Test 4: 3-Node Triangle Graph [[2,3],[1,3],[1,2]]
        int[][] adj4 = {
            {2, 3},
            {1, 3},
            {1, 2}
        };
        Node g4 = buildGraphFromAdjList(adj4);
        testClone("Test 4: 3-Node Triangle Graph", g4);

        System.out.println("\nAll Clone Graph test cases passed successfully!");
    }

    private static void testClone(String label, Node original) {
        Node cloneDFS = cloneGraphDFS(original);
        Node cloneBFS = cloneGraphBFS(original);

        boolean dfsValid = verifyDeepCopy(original, cloneDFS);
        boolean bfsValid = verifyDeepCopy(original, cloneBFS);

        boolean ok = dfsValid && bfsValid;
        System.out.printf("[%s] => DFS Valid: %b | BFS Valid: %b => %s%n",
                label, dfsValid, bfsValid, (ok ? "PASSED" : "FAILED"));

        if (!ok) {
            throw new AssertionError("Clone Graph deep copy failed for " + label);
        }
    }
}
