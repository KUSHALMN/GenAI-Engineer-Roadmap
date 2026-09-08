from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from .copilot_engine import EnterpriseCopilotEngine, CopilotQuery
except ImportError:
    from copilot_engine import EnterpriseCopilotEngine, CopilotQuery

app = FastAPI(
    title="Day 31 Capstone: Enterprise Autonomous Support Copilot",
    description="End-to-end GenAI system combining streaming, RAG, guardrails, routing, and observability.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

copilot = EnterpriseCopilotEngine()

@app.get("/")
def root():
    return {
        "service": "Enterprise Autonomous Support Copilot",
        "milestone": "Month 01 Capstone (Day 31)",
        "capabilities": [
            "SSE Real-Time Streaming",
            "Multi-Tenant Token Bucket Limits",
            "OWASP Prompt Injection Firewall",
            "Two-Stage RAG with Citations",
            "Sub-15ms Semantic Caching",
            "Full Distributed Trace Telemetry"
        ]
    }

@app.post("/api/v1/copilot/chat")
async def copilot_chat(query: CopilotQuery):
    return StreamingResponse(
        copilot.execute_stream(query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
