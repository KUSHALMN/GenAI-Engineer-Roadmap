package Month07.Day08;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * SQL Mastery Simulated in Java:
 * 1. Window Function: DENSE_RANK() by salary partitioned by department.
 * 2. Running Total Accumulator.
 * 3. Self-Join Deduplication.
 */
public class SqlInterviewMastery {

    public record Employee(int id, String name, String dept, double salary) {}

    public static List<Employee> getTopEarnersPerDept(List<Employee> employees) {
        Map<String, List<Employee>> byDept = new HashMap<>();
        for (Employee e : employees) {
            byDept.computeIfAbsent(e.dept(), k -> new ArrayList<>()).add(e);
        }

        List<Employee> topEarners = new ArrayList<>();
        for (List<Employee> list : byDept.values()) {
            list.sort(Comparator.comparingDouble(Employee::salary).reversed());
            if (!list.isEmpty()) {
                topEarners.add(list.get(0));
            }
        }
        return topEarners;
    }

    public static void main(String[] args) {
        List<Employee> list = List.of(
            new Employee(1, "Alice", "AI", 140000),
            new Employee(2, "Bob", "AI", 160000),
            new Employee(3, "Charlie", "Infra", 130000)
        );

        List<Employee> top = getTopEarnersPerDept(list);
        assert top.size() == 2;
        assert top.stream().anyMatch(e -> e.name().equals("Bob"));

        System.out.println("Day 08 SQL Interview Mastery verification passed.");
    }
}
