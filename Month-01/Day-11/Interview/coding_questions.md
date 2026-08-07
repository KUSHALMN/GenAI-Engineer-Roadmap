# Coding Questions — Day 11

## Q1: Implement Queue using Stacks (Java)
```java
Stack<Integer> inbox = new Stack<>();
Stack<Integer> outbox = new Stack<>();

void push(int x) { inbox.push(x); }

int pop() {
    if (outbox.isEmpty())
        while (!inbox.isEmpty()) outbox.push(inbox.pop());
    return outbox.pop();
}

int peek() {
    if (outbox.isEmpty())
        while (!inbox.isEmpty()) outbox.push(inbox.pop());
    return outbox.peek();
}

boolean empty() { return inbox.isEmpty() && outbox.isEmpty(); }
```

## Q2: Number of Recent Calls (Java)
```java
Queue<Integer> queue = new LinkedList<>();

int ping(int t) {
    queue.offer(t);
    while (queue.peek() < t - 3000) queue.poll();
    return queue.size();
}
```

## Q3: Config Pattern (Python)
```python
# config.py
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 200
OVERLAP = 30

# usage in other files
from config import LLM_MODEL, CHUNK_SIZE
```

## Q4: Implement Stack using Queue (Python)
```python
from collections import deque

class Stack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self): return self.q.popleft()
    def top(self): return self.q[0]
    def empty(self): return not self.q
```

## Q5: Sliding Window — Recent Calls (Python)
```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.q = deque()

    def ping(self, t):
        self.q.append(t)
        while self.q[0] < t - 3000:
            self.q.popleft()
        return len(self.q)
```
