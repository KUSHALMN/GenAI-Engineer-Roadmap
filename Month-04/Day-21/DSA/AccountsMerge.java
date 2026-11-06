import java.util.*;

/**
 * Day 21: Disjoint Set Union (DSU) — Accounts Merge
 * Problem: Given a list of accounts where each account has a name and emails,
 * merge accounts belonging to the same person (sharing any email).
 *
 * Algorithm:
 * - Map each email to a unique integer ID.
 * - Union email IDs within the same account.
 * - Group emails by their root parent, sort, and attach account owner name.
 *
 * Time Complexity: O(N * log N) where N is total emails.
 * Space Complexity: O(N)
 */
public class AccountsMerge {

    static class DSU {
        int[] parent;
        DSU(int n) {
            parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]); // Path compression
            return parent[x];
        }
        void union(int x, int y) {
            parent[find(x)] = find(y);
        }
    }

    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        DSU dsu = new DSU(10001);
        Map<String, String> emailToName = new HashMap<>();
        Map<String, Integer> emailToId = new HashMap<>();
        int idCounter = 0;

        for (List<String> acc : accounts) {
            String name = acc.get(0);
            for (int i = 1; i < acc.size(); i++) {
                String email = acc.get(i);
                emailToName.put(email, name);
                if (!emailToId.containsKey(email)) {
                    emailToId.put(email, idCounter++);
                }
                dsu.union(emailToId.get(acc.get(1)), emailToId.get(email));
            }
        }

        Map<Integer, List<String>> groups = new HashMap<>();
        for (String email : emailToId.keySet()) {
            int root = dsu.find(emailToId.get(email));
            groups.computeIfAbsent(root, x -> new ArrayList<>()).add(email);
        }

        List<List<String>> merged = new ArrayList<>();
        for (List<String> component : groups.values()) {
            Collections.sort(component);
            List<String> account = new ArrayList<>();
            account.add(emailToName.get(component.get(0)));
            account.addAll(component);
            merged.add(account);
        }
        return merged;
    }

    public static void main(String[] args) {
        AccountsMerge solver = new AccountsMerge();
        List<List<String>> accounts = Arrays.asList(
            Arrays.asList("John", "johnsmith@mail.com", "john_newyork@mail.com"),
            Arrays.asList("John", "johnsmith@mail.com", "john00@mail.com"),
            Arrays.asList("Mary", "mary@mail.com"),
            Arrays.asList("John", "johnnybravo@mail.com")
        );

        List<List<String>> res = solver.accountsMerge(accounts);
        System.out.println("Merged accounts count: " + res.size());
        assert res.size() == 3 : "Expected 3 distinct individuals";
        System.out.println("Day 21 DSA AccountsMerge verification passed!");
    }
}
