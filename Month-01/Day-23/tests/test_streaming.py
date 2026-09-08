import sys
import os
import pytest

# Ensure src is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from stream_engine import StreamingLLMEngine
from schemas import StreamRequest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_async_engine():
    engine = StreamingLLMEngine()
    req = StreamRequest(prompt="Hello async world", chunk_delay_ms=1)
    tokens = []
    final_metrics = None
    async for payload, metrics in engine.generate_stream(req):
        tokens.append(payload.token)
        if metrics:
            final_metrics = metrics
    assert len(tokens) > 0
    assert final_metrics is not None
    assert final_metrics.total_tokens > 0

def test_sse_endpoint():
    response = client.post("/api/v1/stream/sse", json={"prompt": "Stream test", "chunk_delay_ms": 1})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert "event: token" in response.text
