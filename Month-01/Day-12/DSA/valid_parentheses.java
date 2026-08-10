import java.util.Stack;

public class valid_parentheses {
    // LeetCode #20 - Valid Parentheses
    // Approach: Stack — push open, pop and match on close O(n)
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if (c == ')' && top != '(') return false;
                if (c == '}' && top != '{') return false;
                if (c == ']' && top != '[') return false;
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        valid_parentheses sol = new valid_parentheses();
        System.out.println(sol.isValid("()[]{}"));  // true
        System.out.println(sol.isValid("(]"));       // false
        System.out.println(sol.isValid("{[]}"));     // true
    }
}
