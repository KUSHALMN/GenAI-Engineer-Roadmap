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

app = FastAPI(
    title="Production Streaming LLM & Async API",
    description="Enterprise async token streaming with Server-Sent Events (SSE) and WebSockets.",
    version="1.0.0"
)

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
    return {
        "service": "Streaming LLM API",
        "status": "online",
        "endpoints": {
            "sse": "POST /api/v1/stream/sse",
            "jsonl": "POST /api/v1/stream/jsonl",
            "ws": "WS /ws/stream"
        }
    }

@app.post("/api/v1/stream/sse")
async def stream_sse(request: StreamRequest):
    async def sse_event_generator():
        try:
            async for payload, metrics in engine.generate_stream(request):
                yield f"event: token\ndata: {payload.model_dump_json()}\n\n"
                if metrics:
                    yield f"event: done\ndata: {metrics.model_dump_json()}\n\n"
        except asyncio.CancelledError:
            print("Client disconnected mid-SSE stream")
            raise

    return StreamingResponse(
        sse_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/v1/stream/jsonl")
async def stream_jsonl(request: StreamRequest):
    async def jsonl_generator():
        async for payload, metrics in engine.generate_stream(request):
            data = {"type": "token", "payload": payload.model_dump()}
            if metrics:
                data["metrics"] = metrics.model_dump()
            yield json.dumps(data) + "\n"

    return StreamingResponse(
        jsonl_generator(),
        media_type="application/x-ndjson"
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
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
