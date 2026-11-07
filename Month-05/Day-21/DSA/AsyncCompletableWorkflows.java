import java.util.concurrent.*;

/**
 * Day 21: Concurrency — CompletableFuture Asynchronous Workflows
 * Chaining async pipelines (supplyAsync -> thenApply -> thenCombine).
 */
public class AsyncCompletableWorkflows {

    public static void main(String[] args) throws Exception {
        CompletableFuture<String> fetchUser = CompletableFuture.supplyAsync(() -> "User-42");
        CompletableFuture<Double> fetchQuota = CompletableFuture.supplyAsync(() -> 1500.0);

        CompletableFuture<String> combined = fetchUser.thenCombine(fetchQuota, (user, quota) -> {
            return user + " has remaining quota of " + quota + " tokens.";
        });

        String result = combined.get(1, TimeUnit.SECONDS);
        System.out.println("Async workflow result: " + result);
        assert result.contains("User-42");
        System.out.println("Day 21 DSA AsyncCompletableWorkflows verification passed!");
    }
}
