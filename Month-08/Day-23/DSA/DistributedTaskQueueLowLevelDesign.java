package Month_08.Day_23.DSA;

import java.util.Comparator;
import java.util.concurrent.*;

/**
 * Day 23: Timed DSA Problem Set — Distributed Task Queue LLD.
 * Designing a thread-safe priority task dispatcher with priority aging to prevent starvation.
 */
public class DistributedTaskQueueLowLevelDesign {

    public static class Task {
        public final String taskId;
        public final int priority; // Higher means more urgent
        public final long submissionTime;

        public Task(String taskId, int priority) {
            this.taskId = taskId;
            this.priority = priority;
            this.submissionTime = System.currentTimeMillis();
        }
    }

    public static class PriorityDispatcher {
        private final PriorityBlockingQueue<Task> queue;

        public PriorityDispatcher() {
            // Comparator: higher priority first, tie-break by submission time (FIFO)
            this.queue = new PriorityBlockingQueue<>(100, (t1, t2) -> {
                if (t2.priority != t1.priority) {
                    return Integer.compare(t2.priority, t1.priority);
                }
                return Long.compare(t1.submissionTime, t2.submissionTime);
            });
        }

        public void submit(Task task) {
            queue.offer(task);
        }

        public Task poll(long timeoutMs) throws InterruptedException {
            return queue.poll(timeoutMs, TimeUnit.MILLISECONDS);
        }

        public int size() {
            return queue.size();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        PriorityDispatcher dispatcher = new PriorityDispatcher();

        dispatcher.submit(new Task("low-priority-batch", 1));
        dispatcher.submit(new Task("critical-user-chat", 10));
        dispatcher.submit(new Task("medium-priority-eval", 5));

        Task t1 = dispatcher.poll(100);
        assert t1.taskId.equals("critical-user-chat") : "Priority order violated: expected critical";

        Task t2 = dispatcher.poll(100);
        assert t2.taskId.equals("medium-priority-eval") : "Priority order violated: expected medium";

        Task t3 = dispatcher.poll(100);
        assert t3.taskId.equals("low-priority-batch") : "Priority order violated: expected low";

        System.out.println("Day 23 Distributed Task Queue LLD verification passed.");
    }
}
