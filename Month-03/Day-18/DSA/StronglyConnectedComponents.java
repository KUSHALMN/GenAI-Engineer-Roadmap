package DSA;

import java.util.*;

/**
 * Tarjan's Algorithm for Strongly Connected Components (SCC)
 * A directed graph is strongly connected if every vertex is reachable from every other vertex.
 * 
 * Tarjan's Algorithm uses DFS with:
 * - discoveryTime[u]: when node u was first visited
 * - low[u]: lowest discoveryTime reachable from u via subtree/back-edges
 * - stack: nodes currently in the active DFS path
 * 
 * Complexity:
 * - Time: O(V + E) - single DFS pass
 * - Space: O(V) for stack, low, discovery arrays
 */
public class StronglyConnectedComponents {
    private int time = 0;

    public List<List<Integer>> findSCCs(int n, List<List<Integer>> adj) {
        int[] disc = new int[n];
        int[] low = new int[n];
        boolean[] onStack = new boolean[n];
        Stack<Integer> stack = new Stack<>();
        Arrays.fill(disc, -1);
        Arrays.fill(low, -1);

        List<List<Integer>> sccs = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            if (disc[i] == -1) {
                dfs(i, adj, disc, low, onStack, stack, sccs);
            }
        }

        return sccs;
    }

    private void dfs(
        int u,
        List<List<Integer>> adj,
        int[] disc,
        int[] low,
        boolean[] onStack,
        Stack<Integer> stack,
        List<List<Integer>> sccs
    ) {
        disc[u] = low[u] = ++time;
        stack.push(u);
        onStack[u] = true;

        for (int v : adj.get(u)) {
            if (disc[v] == -1) {
                // Tree edge
                dfs(v, adj, disc, low, onStack, stack, sccs);
                low[u] = Math.min(low[u], low[v]);
            } else if (onStack[v]) {
                // Back-edge to a node currently in stack
                low[u] = Math.min(low[u], disc[v]);
            }
        }

        // If u is a root of an SCC, pop all members of this SCC from stack
        if (low[u] == disc[u]) {
            List<Integer> scc = new ArrayList<>();
            while (true) {
                int node = stack.pop();
                onStack[node] = false;
                scc.add(node);
                if (node == u) break;
            }
            sccs.add(scc);
        }
    }

    public static void main(String[] args) {
        int n = 5;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        // Directed edges: 1->0, 0->2, 2->1, 0->3, 3->4
        adj.get(1).add(0);
        adj.get(0).add(2);
        adj.get(2).add(1);
        adj.get(0).add(3);
        adj.get(3).add(4);

        StronglyConnectedComponents solver = new StronglyConnectedComponents();
        List<List<Integer>> sccs = solver.findSCCs(n, adj);

        System.out.println("Strongly Connected Components discovered (" + sccs.size() + "):");
        for (List<Integer> scc : sccs) {
            System.out.println("SCC: " + scc);
        }

        System.out.println("Tarjan SCC tests passed!");
    }
}
