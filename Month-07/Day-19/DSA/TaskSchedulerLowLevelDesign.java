package Month07.Day19;

import java.util.PriorityQueue;

/**
 * Low-Level Design (LLD): Distributed Task Scheduler
 * PriorityQueue-based delay execution queue prioritizing earlier execution timestamps.
 */
public class TaskSchedulerLowLevelDesign {

    public record ScheduledJob(String jobId, long executeAtMillis, Runnable action)
            implements Comparable<ScheduledJob> {
        @Override
        public int compareTo(ScheduledJob other) {
            return Long.compare(this.executeAtMillis, other.executeAtMillis);
        }
    }

    public static class TaskScheduler {
        private final PriorityQueue<ScheduledJob> queue = new PriorityQueue<>();

        public synchronized void schedule(String id, long delayMillis, Runnable task) {
            queue.add(new ScheduledJob(id, System.currentTimeMillis() + delayMillis, task));
        }

        public synchronized ScheduledJob pollNextExecutable(long now) {
            if (!queue.isEmpty() && queue.peek().executeAtMillis() <= now) {
                return queue.poll();
            }
            return null;
        }

        public synchronized int pendingCount() { return queue.size(); }
    }

    public static void main(String[] args) {
        TaskScheduler scheduler = new TaskScheduler();
        long now = System.currentTimeMillis();
        scheduler.schedule("job-1", 1000, () -> {});
        scheduler.schedule("job-urgent", 50, () -> {});

        ScheduledJob immediate = scheduler.pollNextExecutable(now + 60);
        assert immediate != null;
        assert immediate.jobId().equals("job-urgent");

        System.out.println("Day 19 Task Scheduler LLD verification passed.");
    }
}
