import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from rate_limiter import TokenBucketRateLimiter
from router import DynamicModelRouter

client = TestClient(app)

def test_token_bucket_consumption():
    tb = TokenBucketRateLimiter(rpm_limit=2, tpm_limit=500)
    # First consume
    ok, _ = tb.consume("tenant_a", 100)
    assert ok
    # Second consume
    ok, _ = tb.consume("tenant_a", 100)
    assert ok
    # Third consume should fail RPM
    ok, reason = tb.consume("tenant_a", 100)
    assert not ok
    assert "RPM limit exceeded" in reason

def test_model_router_logic():
    simple_prompt = "What is the capital of Canada?"
    decision_simple = DynamicModelRouter.route_request(simple_prompt)
    assert decision_simple["selected_model"] == DynamicModelRouter.LIGHTWEIGHT_MODEL

    complex_prompt = "Implement a distributed Raft consensus algorithm in Java with state machines."
    decision_complex = DynamicModelRouter.route_request(complex_prompt)
    assert decision_complex["selected_model"] == DynamicModelRouter.FRONTIER_MODEL

def test_api_dispatch_flow():
    res = client.post("/api/v1/gateway/dispatch", json={"prompt": "Hello AI Gateway", "tenant_id": "org_beta"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["tenant_id"] == "org_beta"
    assert "routing" in data
