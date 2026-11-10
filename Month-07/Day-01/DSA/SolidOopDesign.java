package Month07.Day01;

import java.util.ArrayList;
import java.util.List;

/**
 * SOLID OOP Principles Mastery:
 * S - Single Responsibility (Separate storage from notification)
 * O - Open/Closed (Extensible payment processor via interfaces)
 * L - Liskov Substitution (Subclasses cleanly replace parent types)
 * I - Interface Segregation (Lean, task-focused interfaces)
 * D - Dependency Inversion (High-level modules depend on abstractions)
 */
public class SolidOopDesign {

    // Single Responsibility & Interface Segregation
    public interface MessageSender {
        void sendMessage(String recipient, String message);
    }

    public static class EmailSender implements MessageSender {
        @Override
        public void sendMessage(String recipient, String message) {
            // Emulate email dispatch
        }
    }

    // Open/Closed Principle
    public interface PaymentStrategy {
        boolean processPayment(double amount);
    }

    public static class CreditCardPayment implements PaymentStrategy {
        @Override
        public boolean processPayment(double amount) {
            return amount > 0;
        }
    }

    public static class CryptoPayment implements PaymentStrategy {
        @Override
        public boolean processPayment(double amount) {
            return amount > 0;
        }
    }

    // Dependency Inversion: CheckoutService depends on abstractions
    public static class CheckoutService {
        private final PaymentStrategy paymentStrategy;
        private final MessageSender messageSender;

        public CheckoutService(PaymentStrategy paymentStrategy, MessageSender messageSender) {
            this.paymentStrategy = paymentStrategy;
            this.messageSender = messageSender;
        }

        public boolean checkout(String customerEmail, double amount) {
            if (paymentStrategy.processPayment(amount)) {
                messageSender.sendMessage(customerEmail, "Order confirmed for $" + amount);
                return true;
            }
            return false;
        }
    }

    public static void main(String[] args) {
        PaymentStrategy card = new CreditCardPayment();
        MessageSender email = new EmailSender();
        CheckoutService service = new CheckoutService(card, email);

        boolean result = service.checkout("kushal@example.com", 150.00);
        assert result;
        System.out.println("Day 01 SOLID OOP Design verification passed: " + result);
    }
}
