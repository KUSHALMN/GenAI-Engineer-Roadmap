import java.util.Stack;

public class implement_queue_using_stacks {
    // LeetCode #232 - Implement Queue using Stacks
    // Approach: Two Stacks — Amortized O(1)
    private Stack<Integer> inbox  = new Stack<>();
    private Stack<Integer> outbox = new Stack<>();

    public void push(int x) {
        inbox.push(x);
    }

    public int pop() {
        transfer();
        return outbox.pop();
    }

    public int peek() {
        transfer();
        return outbox.peek();
    }

    public boolean empty() {
        return inbox.isEmpty() && outbox.isEmpty();
    }

    private void transfer() {
        if (outbox.isEmpty()) {
            while (!inbox.isEmpty())
                outbox.push(inbox.pop());
        }
    }

    public static void main(String[] args) {
        implement_queue_using_stacks q = new implement_queue_using_stacks();
        q.push(1);
        q.push(2);
        System.out.println(q.peek()); // 1
        System.out.println(q.pop());  // 1
        System.out.println(q.empty()); // false
    }
}
