public class best_time_to_buy_stock {
    // LeetCode #121 - Best Time to Buy and Sell Stock
    // Approach: Sliding Window / Greedy O(n)
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;

        for (int price : prices) {
            if (price < minPrice)
                minPrice = price;
            else if (price - minPrice > maxProfit)
                maxProfit = price - minPrice;
        }
        return maxProfit;
    }

    public static void main(String[] args) {
        best_time_to_buy_stock sol = new best_time_to_buy_stock();
        System.out.println(sol.maxProfit(new int[]{7, 1, 5, 3, 6, 4})); // 5
        System.out.println(sol.maxProfit(new int[]{7, 6, 4, 3, 1}));    // 0
    }
}
