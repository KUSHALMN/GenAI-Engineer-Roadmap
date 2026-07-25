public class first_bad_version {
    // LeetCode #278 - First Bad Version
    // Approach: Binary Search O(log n)

    private int bad; // simulated bad version

    boolean isBadVersion(int version) {
        return version >= bad;
    }

    public int firstBadVersion(int n) {
        int left = 1, right = n;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (isBadVersion(mid)) right = mid;
            else left = mid + 1;
        }
        return left;
    }

    public static void main(String[] args) {
        first_bad_version sol = new first_bad_version();
        sol.bad = 4;
        System.out.println(sol.firstBadVersion(5)); // 4

        sol.bad = 1;
        System.out.println(sol.firstBadVersion(1)); // 1
    }
}
