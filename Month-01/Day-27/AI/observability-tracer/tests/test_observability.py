import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app, tracer
from tracer import ObservabilityTracer

client = TestClient(app)

def test_span_lifecycle():
    local_tracer = ObservabilityTracer()
    with local_tracer.start_span("test_span", "gpt-4o") as span:
        span.prompt_tokens = 500
        span.completion_tokens = 200

    assert len(local_tracer.spans) == 1
    s = local_tracer.spans[0]
    assert s.total_tokens == 700
    assert s.estimated_cost_usd > 0
    assert s.status == "ok"
    assert s.duration_ms >= 0

def test_percentile_calculation():
    local_tracer = ObservabilityTracer()
    for i in range(1, 101):
        with local_tracer.start_span("batch", "gpt-4o-mini") as span:
            span.duration_ms = float(i)
    
    # Override sorted durations for pure mathematical check
    for idx, s in enumerate(local_tracer.spans):
        s.duration_ms = float(idx + 1)

    pct = local_tracer.get_latency_percentiles()
    assert pct["p50"] >= 49.0 and pct["p50"] <= 52.0
    assert pct["p95"] >= 94.0
    assert pct["p99"] >= 98.0

def test_api_generate_and_metrics():
    res = client.post("/api/v1/generate", json={"prompt": "Explain LLM latency percentiles", "model": "gpt-4o-mini"})
    assert res.status_code == 200
    data = res.json()
    assert "telemetry" in data
    assert data["telemetry"]["prompt_tokens"] > 0

    metrics_res = client.get("/api/v1/metrics")
    assert metrics_res.status_code == 200
    metrics_data = metrics_res.json()
    assert metrics_data["total_calls"] >= 1
    assert "latency_percentiles_ms" in metrics_data
