import java.util.*;
import java.util.stream.*;

/**
 * Day 06: Java Streams & Collection Pipelines
 * Demonstrates declarative data manipulation: filter, map, flatMap, reduce, groupingBy.
 * Compares stream readability against iterative loop performance.
 */
public class StreamPipelines {

    static class Transaction {
        String category;
        double amount;
        Transaction(String category, double amount) { this.category = category; this.amount = amount; }
    }

    public static void main(String[] args) {
        List<Transaction> txs = Arrays.asList(
            new Transaction("AI", 120.0),
            new Transaction("Cloud", 450.0),
            new Transaction("AI", 80.0),
            new Transaction("Hardware", 900.0)
        );

        // Group total spend by category
        Map<String, Double> spendByCategory = txs.stream()
            .collect(Collectors.groupingBy(
                t -> t.category,
                Collectors.summingDouble(t -> t.amount)
            ));

        assert spendByCategory.get("AI") == 200.0;
        assert spendByCategory.get("Cloud") == 450.0;

        // Top spend filtering
        List<String> highSpendCategories = spendByCategory.entrySet().stream()
            .filter(e -> e.getValue() > 150.0)
            .map(Map.Entry::getKey)
            .sorted()
            .collect(Collectors.toList());

        assert highSpendCategories.contains("AI") && highSpendCategories.contains("Cloud");
        System.out.println("Spend by Category: " + spendByCategory);
        System.out.println("High spend categories: " + highSpendCategories);
        System.out.println("Day 06 DSA StreamPipelines verification passed!");
    }
}
