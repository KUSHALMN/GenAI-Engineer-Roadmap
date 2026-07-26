from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
from models import ChatRequest, ChatResponse
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# In-memory session store
sessions: dict[str, list] = {}

@app.get("/")
def root():
    return {"message": "AI Chat API is running!"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = sessions.get(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."}] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    sessions[req.session_id] = history

    return ChatResponse(reply=reply, session_id=req.session_id)

@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"message": f"Session '{session_id}' cleared."}

# Run: uvicorn app:app --reload
# Docs: http://127.0.0.1:8000/docs
