# Month 1 - Day 5

## Topics Learned
- FastAPI Basics (Path params, Query params, Request body)
- Pydantic Models for validation
- REST API design
- Binary Search on Rotated Arrays

## Python
- Hello FastAPI (GET endpoints, path & query params)
- Calculator API (POST endpoints, Pydantic, error handling)

## DSA (Java)
- Find Minimum in Rotated Sorted Array — LeetCode #153
- Search in Rotated Sorted Array — LeetCode #33
- Peak Index in Mountain Array — LeetCode #852

## AI Project
- AI Chat API (FastAPI + Groq + session-based history)

## What I Learned
Today I built my first FastAPI applications and learned how to expose AI models as REST APIs. On the DSA side, I mastered binary search variants on rotated and mountain arrays.

## API Endpoints — AI Chat API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Send message, get AI reply |
| DELETE | `/chat/{session_id}` | Clear conversation history |

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is RAG?", "session_id": "user1"}'
```

---

## Folder Structure

```
Day-05/
├── Python/
│   ├── hello_fastapi.py
│   └── calculator_api.py
├── DSA/
│   ├── find_min_rotated.java
│   ├── search_rotated_array.java
│   └── peak_index_mountain.java
├── AI/
│   └── ai_chat_api/
│       ├── app.py
│       ├── models.py
│       └── README.md
├── Notes/
│   └── day5_notes.md
├── Resources.md
└── README.md
```

## How to Run

**Python:**
```bash
pip install fastapi uvicorn
uvicorn Python/hello_fastapi:app --reload
uvicorn Python/calculator_api:app --reload
```

**DSA (Java):**
```bash
javac DSA/find_min_rotated.java && java -cp DSA find_min_rotated
javac DSA/search_rotated_array.java && java -cp DSA search_rotated_array
javac DSA/peak_index_mountain.java && java -cp DSA peak_index_mountain
```

**AI Chat API:**
```bash
cd AI/ai_chat_api
pip install fastapi uvicorn groq python-dotenv
# Create .env with: GROQ_API_KEY=your_key_here
uvicorn app:app --reload
```
