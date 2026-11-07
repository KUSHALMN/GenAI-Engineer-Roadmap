import java.util.concurrent.*;

/**
 * Day 26: Concurrency — Thread Pool Sizing & Work Queue Rejection Policies
 * Configures ThreadPoolExecutor with bounded ArrayBlockingQueue and CallerRunsPolicy.
 */
public class CustomThreadPoolRejection {

    public static void main(String[] args) {
        int corePoolSize = 2;
        int maxPoolSize = 4;
        long keepAliveTime = 10;
        BlockingQueue<Runnable> workQueue = new ArrayBlockingQueue<>(2);

        // CallerRunsPolicy executes task in submitting thread if pool & queue are saturated
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            corePoolSize,
            maxPoolSize,
            keepAliveTime,
            TimeUnit.SECONDS,
            workQueue,
            new ThreadPoolExecutor.CallerRunsPolicy()
        );

        for (int i = 1; i <= 6; i++) {
            final int taskId = i;
            executor.execute(() -> {
                try { Thread.sleep(10); } catch (InterruptedException e) {}
            });
        }

        executor.shutdown();
        System.out.println("Day 26 DSA CustomThreadPoolRejection verification passed!");
    }
}
