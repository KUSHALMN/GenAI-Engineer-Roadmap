from fastapi import FastAPI
from fastapi.responses import StreamingResponse

try:
    from .copilot_engine import EnterpriseCopilotEngine, CopilotQuery
except ImportError:
    from copilot_engine import EnterpriseCopilotEngine, CopilotQuery

app = FastAPI(title="Enterprise Support Copilot - Day 31")
copilot = EnterpriseCopilotEngine()

@app.get("/")
def root():
    return {"service": "Enterprise Autonomous Support Copilot", "status": "online"}

@app.post("/api/v1/copilot/chat")
async def copilot_chat(query: CopilotQuery):
    return StreamingResponse(
        copilot.execute_stream(query),
        media_type="text/event-stream"
    )
