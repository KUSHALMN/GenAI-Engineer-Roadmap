# Coding Questions — Day 13

## Java — Stack (Hard)

### Largest Rectangle in Histogram (Hard)
```java
// Monotonic increasing stack
Stack<Integer> stack = new Stack<>();
for (int i = 0; i <= n; i++) {
    int h = (i == n) ? 0 : heights[i];
    while (!stack.isEmpty() && h < heights[stack.peek()]) {
        int height = heights[stack.pop()];
        int width = stack.isEmpty() ? i : i - stack.peek() - 1;
        maxArea = Math.max(maxArea, height * width);
    }
    stack.push(i);
}
```

### Daily Temperatures (Medium)
```java
// Monotonic decreasing stack of indices
while (!stack.isEmpty() && temps[i] > temps[stack.peek()])
    result[stack.pop()] = i - idx;
stack.push(i);
```

## Python — RAG Modular Design

### How to lazy-load embedding model?
```python
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model
```

### How to write a minimal pytest test?
```python
def test_split_text():
    chunks = split_text("a" * 1200)
    assert len(chunks) > 1
```
