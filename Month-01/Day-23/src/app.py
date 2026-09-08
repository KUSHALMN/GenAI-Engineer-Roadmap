import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from .schemas import StreamRequest, StreamTokenPayload, StreamMetrics
    from .stream_engine import StreamingLLMEngine
except ImportError:
    from schemas import StreamRequest, StreamTokenPayload, StreamMetrics
    from stream_engine import StreamingLLMEngine

app = FastAPI(title="LLM Streaming API - Day 23")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = StreamingLLMEngine()

@app.get("/")
async def root():
    return {"status": "online", "message": "Day 23: LLM Streaming + Async APIs", "endpoints": {"sse": "/api/v1/stream/sse"}}

@app.post("/api/v1/stream/sse")
async def stream_sse(request: StreamRequest):
    async def sse_event_generator():
        async for payload, metrics in engine.generate_stream(request):
            yield f"event: token\ndata: {payload.model_dump_json()}\n\n"
            if metrics:
                yield f"event: done\ndata: {metrics.model_dump_json()}\n\n"

    return StreamingResponse(
        sse_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()
            req = StreamRequest(**json.loads(raw_data))
            async for payload, metrics in engine.generate_stream(req):
                msg = {"event": "token", "data": payload.model_dump()}
                if metrics:
                    msg["metrics"] = metrics.model_dump()
                await websocket.send_text(json.dumps(msg))
    except WebSocketDisconnect:
        pass
