import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from rate_limiter import TokenBucketRateLimiter
from router import DynamicModelRouter

client = TestClient(app)

def test_rate_limiter():
    tb = TokenBucketRateLimiter(rpm_limit=1, tpm_limit=200)
    ok, _ = tb.consume("t1", 50)
    assert ok
    ok, err = tb.consume("t1", 50)
    assert not ok

def test_routing():
    res = DynamicModelRouter.route_request("Write code for binary search")
    assert res["selected_model"] == "gpt-4o"

def test_api_dispatch():
    res = client.post("/api/v1/gateway/dispatch", json={"prompt": "Short prompt", "tenant_id": "client_1"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"
