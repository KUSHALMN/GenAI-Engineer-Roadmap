# Coding Questions — Day 12

## Java — Stack

### Valid Parentheses (Easy)
```java
// Use stack, push open brackets, pop and match on close
Stack<Character> stack = new Stack<>();
for (char c : s.toCharArray()) {
    if (c == '(' || c == '{' || c == '[') stack.push(c);
    else {
        if (stack.isEmpty()) return false;
        char top = stack.pop();
        if (c == ')' && top != '(') return false;
    }
}
return stack.isEmpty();
```

### Daily Temperatures (Medium)
```java
// Monotonic decreasing stack of indices
Stack<Integer> stack = new Stack<>();
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && temps[i] > temps[stack.peek()])
        result[stack.pop()] = i - stack.peek(); // wrong, fix:
    stack.push(i);
}
```

### Evaluate RPN (Medium)
```java
// Push numbers, pop two on operator
switch (token) {
    case "+" -> stack.push(stack.pop() + stack.pop());
    case "-" -> { int b = stack.pop(), a = stack.pop(); stack.push(a - b); }
}
```

## Python — RAG

### How to chunk text with overlap?
```python
chunks, start = [], 0
while start < len(text):
    chunks.append(text[start:start + CHUNK_SIZE])
    start += CHUNK_SIZE - CHUNK_OVERLAP
```
