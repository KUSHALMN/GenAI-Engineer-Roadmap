# Coding Questions — Day 10

## Q1: Valid Parentheses (Java)
```java
public boolean isValid(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '{' || c == '[') stack.push(c);
        else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if (c == ')' && top != '(') return false;
            if (c == '}' && top != '{') return false;
            if (c == ']' && top != '[') return false;
        }
    }
    return stack.isEmpty();
}
```

## Q2: Min Stack (Java)
```java
Stack<Integer> stack = new Stack<>();
Stack<Integer> minStack = new Stack<>();

void push(int val) {
    stack.push(val);
    if (minStack.isEmpty() || val <= minStack.peek()) minStack.push(val);
}
void pop() {
    if (stack.pop().equals(minStack.peek())) minStack.pop();
}
int getMin() { return minStack.peek(); }
```

## Q3: Run RAG Chain (Python)
```python
def run_chain(question, n_results=3):
    context_chunks = retrieve(question, n_results)
    messages = build_prompt(question, context_chunks)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return {
        "question": question,
        "context": context_chunks,
        "answer": response.choices[0].message.content
    }
```

## Q4: Paragraph Splitter (Python)
```python
import re

def split_by_paragraphs(text):
    paragraphs = re.split(r'\n{2,}', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]
```

## Q5: Implement a Stack using a List (Python)
```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, val): self._data.append(val)
    def pop(self): return self._data.pop()
    def peek(self): return self._data[-1]
    def is_empty(self): return len(self._data) == 0
```

## Q6: Balanced Brackets Check (Python)
```python
def is_balanced(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in mapping:
            if not stack or stack[-1] != mapping[c]: return False
            stack.pop()
        else:
            stack.append(c)
    return not stack
```
