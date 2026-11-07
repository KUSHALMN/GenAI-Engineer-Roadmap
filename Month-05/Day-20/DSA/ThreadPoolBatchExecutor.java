import java.util.*;
import java.util.concurrent.*;

/**
 * Day 20: Concurrency — ExecutorService & Futures Batching
 * Dispatches concurrent async tasks to a thread pool and collects future results.
 */
public class ThreadPoolBatchExecutor {

    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(3);
        List<Callable<String>> tasks = Arrays.asList(
            () -> { Thread.sleep(20); return "Batch-A"; },
            () -> { Thread.sleep(10); return "Batch-B"; },
            () -> { Thread.sleep(15); return "Batch-C"; }
        );

        List<Future<String>> futures = executor.invokeAll(tasks);
        List<String> results = new ArrayList<>();
        for (Future<String> f : futures) {
            results.add(f.get());
        }

        executor.shutdown();
        assert results.containsAll(Arrays.asList("Batch-A", "Batch-B", "Batch-C"));
        System.out.println("Collected batch results: " + results);
        System.out.println("Day 20 DSA ThreadPoolBatchExecutor verification passed!");
    }
}
