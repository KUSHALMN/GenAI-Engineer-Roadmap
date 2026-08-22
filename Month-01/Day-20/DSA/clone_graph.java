import java.util.*;

/**
 * Problem: Clone Graph (LeetCode 133)
 * 
 * Given a reference of a node in a connected undirected graph.
 * Return a deep copy (clone) of the graph.
 * Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
 * 
 * Approaches:
 * 1. Depth-First Search (DFS) - Recursive:
 *    - Maintain a HashMap<Node, Node> mapping original node -> cloned node.
 *    - For each neighbor, recursively clone and attach to the clone's neighbors list.
 *    - Time Complexity: O(V + E) where V is number of vertices and E is number of edges.
 *    - Space Complexity: O(V) for recursion stack + visited map.
 * 
 * 2. Breadth-First Search (BFS) - Iterative:
 *    - Use a Queue<Node> to traverse node by node.
 *    - Clone node on discovery, register in HashMap, iterate neighbors.
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V) for queue + visited map.
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

        // Iterate through all neighbors
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

        // Initialize clone for root
        Node rootClone = new Node(node.val);
        visited.put(node, rootClone);
        queue.offer(node);

        while (!queue.isEmpty()) {
            Node curr = queue.poll();

            for (Node neighbor : curr.neighbors) {
                if (!visited.containsKey(neighbor)) {
                    // Clone neighbor
                    visited.put(neighbor, new Node(neighbor.val));
                    queue.offer(neighbor);
                }
                // Add cloned neighbor to current cloned node's adjacency list
                visited.get(curr).neighbors.add(visited.get(neighbor));
            }
        }

        return rootClone;
    }

    // ==========================================
    // Graph Helpers for Building & Validating
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

    public static int[][] convertGraphToAdjList(Node node) {
        if (node == null) {
            return new int[0][0];
        }

        Map<Integer, List<Integer>> adj = new TreeMap<>();
        Set<Node> visited = new HashSet<>();
        Queue<Node> queue = new LinkedList<>();

        queue.offer(node);
        visited.add(node);

        while (!queue.isEmpty()) {
            Node curr = queue.poll();
            adj.putIfAbsent(curr.val, new ArrayList<>());

            for (Node neighbor : curr.neighbors) {
                adj.get(curr.val).add(neighbor.val);
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }

        int[][] result = new int[adj.size()][];
        int idx = 0;
        for (Map.Entry<Integer, List<Integer>> entry : adj.entrySet()) {
            List<Integer> list = entry.getValue();
            result[idx] = new int[list.size()];
            for (int i = 0; i < list.size(); i++) {
                result[idx][i] = list.get(i);
            }
            idx++;
        }
        return result;
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

            // 1. Must have same value
            if (o.val != c.val) return false;
            // 2. Must NOT be the same memory reference (deep copy check)
            if (o == c) return false;
            // 3. Must have same number of neighbors
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
    // Verification & Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("      LeetCode 133: Clone Graph Test Suite       ");
        System.out.println("=================================================\n");

        // Test Case 1: 4-node Cycle [[2,4],[1,3],[2,4],[1,3]]
        int[][] adj1 = {
            {2, 4}, // Node 1
            {1, 3}, // Node 2
            {2, 4}, // Node 3
            {1, 3}  // Node 4
        };
        Node g1 = buildGraphFromAdjList(adj1);
        testClone("Test Case 1 (4-Node Cycle)", g1);

        // Test Case 2: Single Node [[]]
        int[][] adj2 = {{}};
        Node g2 = buildGraphFromAdjList(adj2);
        testClone("Test Case 2 (Single Isolated Node)", g2);

        // Test Case 3: Empty Graph []
        testClone("Test Case 3 (Null/Empty Graph)", null);

        // Test Case 4: Triangle Graph [[2,3],[1,3],[1,2]]
        int[][] adj4 = {
            {2, 3},
            {1, 3},
            {1, 2}
        };
        Node g4 = buildGraphFromAdjList(adj4);
        testClone("Test Case 4 (3-Node Triangle)", g4);

        System.out.println("\nAll Clone Graph test cases passed successfully!");
    }

    private static void testClone(String label, Node original) {
        Node cloneDFS = cloneGraphDFS(original);
        Node cloneBFS = cloneGraphBFS(original);

        boolean dfsValid = verifyDeepCopy(original, cloneDFS);
        boolean bfsValid = verifyDeepCopy(original, cloneBFS);

        System.out.printf("[%s] => DFS Valid Deep Copy: %s | BFS Valid Deep Copy: %s => %s%n",
                label, dfsValid, bfsValid, (dfsValid && bfsValid ? "PASSED" : "FAILED"));

        if (!dfsValid || !bfsValid) {
            throw new AssertionError("Deep copy verification failed for: " + label);
        }
    }
}
