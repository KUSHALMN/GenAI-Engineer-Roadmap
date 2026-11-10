package Month07.Day24;

import java.util.List;

/**
 * Code Review & Refactoring Mock:
 * Refactoring imperative, mutation-heavy loops into clean declarative Java Streams.
 */
public class CodeReviewRefactoringMock {

    public static List<String> getActiveAdminUsernames(List<User> users) {
        return users.stream()
                .filter(User::isActive)
                .filter(u -> "ADMIN".equalsIgnoreCase(u.role()))
                .map(User::username)
                .toList();
    }

    public record User(String username, boolean isActive, String role) {}

    public static void main(String[] args) {
        List<User> list = List.of(
            new User("alice", true, "ADMIN"),
            new User("bob", false, "ADMIN"),
            new User("charlie", true, "MEMBER")
        );

        List<String> admins = getActiveAdminUsernames(list);
        assert admins.size() == 1;
        assert admins.get(0).equals("alice");

        System.out.println("Day 24 Code Review & Refactoring verification passed.");
    }
}
