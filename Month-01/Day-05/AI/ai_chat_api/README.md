# AI Chat API

A FastAPI-based chat API powered by Groq LLaMA 3.3 70B with session-based conversation history.

## Setup

```bash
pip install fastapi uvicorn groq python-dotenv
```

Create `.env`:
```
GROQ_API_KEY=your_key_here
```

## Run

```bash
uvicorn app:app --reload
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Send a message |
| DELETE | `/chat/{session_id}` | Clear session history |

## Example Request

```json
POST /chat
{
  "message": "What is RAG?",
  "session_id": "user_1"
}
```

## Docs
Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.
