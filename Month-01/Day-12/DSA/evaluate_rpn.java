import java.util.Stack;

public class evaluate_rpn {
    // LeetCode #150 - Evaluate Reverse Polish Notation
    // Approach: Stack — push numbers, pop two on operator O(n)
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String t : tokens) {
            switch (t) {
                case "+" -> stack.push(stack.pop() + stack.pop());
                case "-" -> { int b = stack.pop(), a = stack.pop(); stack.push(a - b); }
                case "*" -> stack.push(stack.pop() * stack.pop());
                case "/" -> { int b = stack.pop(), a = stack.pop(); stack.push(a / b); }
                default  -> stack.push(Integer.parseInt(t));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        evaluate_rpn sol = new evaluate_rpn();
        System.out.println(sol.evalRPN(new String[]{"2","1","+","3","*"}));         // 9
        System.out.println(sol.evalRPN(new String[]{"4","13","5","/","+"}));        // 6
        System.out.println(sol.evalRPN(new String[]{"10","6","9","3","+","-11","*","/","*","17","+","5","+"})); // 22
    }
}
