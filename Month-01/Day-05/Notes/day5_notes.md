# Day 5 Notes — GenAI Engineer Roadmap

## Topics Learned

### FastAPI Basics
- **FastAPI** — modern, fast Python web framework for building APIs
- **Pydantic** — data validation using Python type hints
- **Uvicorn** — ASGI server to run FastAPI apps
- **Swagger UI** — auto-generated docs at `/docs`
- **Path params** — `/hello/{name}`
- **Query params** — `/items?skip=0&limit=10`
- **Request body** — using `BaseModel` with POST requests

---

## Python Practice

### Hello FastAPI
- Created basic GET endpoints with path and query params
- Auto docs available at `http://127.0.0.1:8000/docs`

### Calculator API
- POST endpoints with Pydantic request body
- HTTPException for error handling (divide by zero)

---

## DSA (Java)

### Find Minimum in Rotated Sorted Array — LeetCode #153
- Approach: Binary Search O(log n)
- If `nums[mid] > nums[right]` → min is in right half
- Else → min is in left half (including mid)

### Search in Rotated Sorted Array — LeetCode #33
- Approach: Binary Search O(log n)
- Determine which half is sorted, then check if target is in that half

### Peak Index in Mountain Array — LeetCode #852
- Approach: Binary Search O(log n)
- If `arr[mid] < arr[mid+1]` → peak is to the right
- Else → peak is at mid or to the left

---

## AI Project — AI Chat API

- Built a REST API with FastAPI + Groq
- Session-based conversation history stored in memory
- Pydantic models for request/response validation
- DELETE endpoint to clear session history

---

## Key Takeaway
FastAPI makes building production-ready APIs incredibly fast. Binary search on rotated arrays requires identifying which half is sorted first — that's the key insight.

---

## FastAPI Cheatsheet

```python
# GET with path param
@app.get("/user/{id}")
def get_user(id: int): ...

# GET with query param
@app.get("/search")
def search(q: str, limit: int = 10): ...

# POST with body
@app.post("/create")
def create(data: BaseModel): ...

# Error handling
raise HTTPException(status_code=404, detail="Not found")
```

## Binary Search Template (Java)

```java
int left = 0, right = nums.length - 1;
while (left <= right) {
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
}
return -1;
```
