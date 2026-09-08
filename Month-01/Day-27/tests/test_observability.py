import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from tracer import ObservabilityTracer

client = TestClient(app)

def test_tracer_span():
    tracer = ObservabilityTracer()
    with tracer.start_span("test", "gpt-4o") as span:
        span.prompt_tokens = 100
        span.completion_tokens = 50
    assert len(tracer.spans) == 1
    assert tracer.spans[0].total_tokens == 150
    assert tracer.spans[0].estimated_cost_usd > 0

def test_percentile_math():
    tracer = ObservabilityTracer()
    for i in range(1, 101):
        with tracer.start_span("batch", "gpt-4o-mini") as span:
            span.duration_ms = float(i)
    # Ensure sequential durations
    for idx, s in enumerate(tracer.spans):
        s.duration_ms = float(idx + 1)
    pct = tracer.get_latency_percentiles()
    assert pct["p50"] >= 49.0
    assert pct["p95"] >= 94.0

def test_api_metrics():
    res = client.post("/api/v1/generate", json={"prompt": "Trace test", "model": "gpt-4o-mini"})
    assert res.status_code == 200
    m_res = client.get("/api/v1/metrics")
    assert m_res.status_code == 200
    assert m_res.json()["total_calls"] >= 1
