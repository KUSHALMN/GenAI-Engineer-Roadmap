import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from stream_engine import StreamingLLMEngine
from schemas import StreamRequest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "sse" in data["endpoints"]

@pytest.mark.asyncio
async def test_stream_engine_generation():
    engine = StreamingLLMEngine()
    req = StreamRequest(prompt="Test Prompt", chunk_delay_ms=1)
    tokens = []
    final_metrics = None
    
    async for payload, metrics in engine.generate_stream(req):
        tokens.append(payload.token)
        if metrics:
            final_metrics = metrics
            
    assert len(tokens) > 0
    assert final_metrics is not None
    assert final_metrics.completion_tokens == len(tokens)
    assert final_metrics.time_to_first_token_ms >= 0

def test_sse_endpoint_stream():
    payload = {"prompt": "Explain LLM streaming in production", "chunk_delay_ms": 1}
    response = client.post("/api/v1/stream/sse", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    text = response.text
    assert "event: token" in text
    assert "event: done" in text
