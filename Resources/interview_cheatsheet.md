# Interview Prep Cheatsheet — Month 01

## GenAI Questions

| Question | Answer |
|----------|--------|
| What is RAG? | Retrieval Augmented Generation — fetch docs + LLM generate |
| What is an embedding? | Dense vector representing semantic meaning of text |
| What is cosine similarity? | Measures angle between two vectors — closer to 1 = more similar |
| What is ChromaDB? | Open-source vector database for semantic search |
| What is a token? | Smallest unit of text an LLM processes |
| What is prompt engineering? | Crafting inputs to guide LLM output effectively |
| Zero-shot vs Few-shot? | Zero-shot = no examples, Few-shot = 2-3 examples provided |

---

## Python Questions

| Question | Answer |
|----------|--------|
| What is a decorator? | Function that wraps another to add behavior |
| What is a context manager? | Manages resources with `with` statement |
| List vs Tuple? | List is mutable, Tuple is immutable |
| `*args` vs `**kwargs`? | `*args` = positional args, `**kwargs` = keyword args |
| What is a generator? | Function that yields values lazily using `yield` |

---

## FastAPI Questions

| Question | Answer |
|----------|--------|
| What is Pydantic? | Data validation using Python type hints |
| GET vs POST? | GET retrieves data, POST sends data in body |
| What is Uvicorn? | ASGI server to run FastAPI apps |
| How to handle errors? | `raise HTTPException(status_code=404, detail="...")` |

---

## SQL Questions

| Question | Answer |
|----------|--------|
| DELETE vs DROP? | DELETE removes rows, DROP removes entire table |
| What is PRIMARY KEY? | Unique + NOT NULL identifier for each row |
| What is SERIAL? | Auto-incrementing integer in PostgreSQL |
| WHERE vs HAVING? | WHERE filters rows, HAVING filters groups |

---

## Coding Patterns (Java)

```java
// Two Sum — HashMap
HashMap<Integer, Integer> map = new HashMap<>();
int complement = target - nums[i];
if (map.containsKey(complement)) return new int[]{map.get(complement), i};
map.put(nums[i], i);

// Sliding Window
int left = 0;
HashSet<Character> set = new HashSet<>();
for (int right = 0; right < s.length(); right++) {
    while (set.contains(s.charAt(right))) set.remove(s.charAt(left++));
    set.add(s.charAt(right));
    max = Math.max(max, right - left + 1);
}

// Binary Search
int left = 0, right = nums.length - 1;
while (left <= right) {
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
}
```
