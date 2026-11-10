package Month07.Day20;

import java.util.ArrayList;
import java.util.List;

/**
 * Low-Level Design (LLD): Notification Service
 * Multi-channel dispatch (Email, SMS, Push) with user preference checks.
 */
public class NotificationServiceLowLevelDesign {

    public enum Channel { EMAIL, SMS, PUSH }

    public interface ChannelSender {
        Channel getChannel();
        boolean send(String recipient, String message);
    }

    public static class NotificationDispatcher {
        private final List<ChannelSender> senders = new ArrayList<>();

        public void registerSender(ChannelSender sender) { senders.add(sender); }

        public boolean dispatch(Channel preferredChannel, String recipient, String message) {
            for (ChannelSender s : senders) {
                if (s.getChannel() == preferredChannel) {
                    return s.send(recipient, message);
                }
            }
            return false;
        }
    }

    public static void main(String[] args) {
        NotificationDispatcher dispatcher = new NotificationDispatcher();
        dispatcher.registerSender(new ChannelSender() {
            @Override public Channel getChannel() { return Channel.EMAIL; }
            @Override public boolean send(String r, String m) { return true; }
        });

        boolean dispatched = dispatcher.dispatch(Channel.EMAIL, "kushal@example.com", "Cluster degraded alert");
        assert dispatched;

        System.out.println("Day 20 Notification Service LLD verification passed.");
    }
}
