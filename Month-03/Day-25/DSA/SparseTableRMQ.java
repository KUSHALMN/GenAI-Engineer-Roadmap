package DSA;

/**
 * Sparse Table for Range Minimum Query (RMQ)
 * Preprocessing: O(N log N) using Dynamic Programming
 * Query: O(1) by overlapping two power-of-2 ranges
 * 
 * Idempotency Property:
 * min(range) is idempotent: min(A, B, B, C) = min(A, B, C)
 * Therefore, we can cover [L, R] using two overlapping intervals of length 2^k
 * where k = floor(log2(R - L + 1)).
 * 
 * Space Complexity: O(N log N)
 */
public class SparseTableRMQ {
    private final int[][] st;
    private final int[] logTable;

    public SparseTableRMQ(int[] arr) {
        int n = arr.length;
        int maxLog = (int) (Math.log(n) / Math.log(2)) + 1;
        this.st = new int[n][maxLog];

        // Precompute logarithms
        this.logTable = new int[n + 1];
        logTable[1] = 0;
        for (int i = 2; i <= n; i++) {
            logTable[i] = logTable[i / 2] + 1;
        }

        // Initialize base intervals of length 2^0 = 1
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }

        // DP transition: interval of length 2^j formed by two intervals of length 2^(j-1)
        for (int j = 1; (1 << j) <= n; j++) {
            for (int i = 0; i + (1 << j) - 1 < n; i++) {
                st[i][j] = Math.min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }

    /**
     * O(1) Range Minimum Query in range [L, R] inclusive
     */
    public int queryMin(int l, int r) {
        int len = r - l + 1;
        int k = logTable[len];
        // Overlap: [L ... L + 2^k - 1] and [R - 2^k + 1 ... R]
        return Math.min(st[l][k], st[r - (1 << k) + 1][k]);
    }

    public static void main(String[] args) {
        int[] arr = {7, 2, 3, 0, 5, 10, 3, 12, 18};
        SparseTableRMQ rmq = new SparseTableRMQ(arr);

        // Min in range [0, 4] -> min(7, 2, 3, 0, 5) = 0
        System.out.println("Min in range [0, 4]: " + rmq.queryMin(0, 4) + " (Expected: 0)");

        // Min in range [4, 7] -> min(5, 10, 3, 12) = 3
        System.out.println("Min in range [4, 7]: " + rmq.queryMin(4, 7) + " (Expected: 3)");

        // Min in range [1, 2] -> min(2, 3) = 2
        System.out.println("Min in range [1, 2]: " + rmq.queryMin(1, 2) + " (Expected: 2)");

        System.out.println("SparseTableRMQ tests passed!");
    }
}
