from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

try:
    from .rate_limiter import TokenBucketRateLimiter
    from .router import DynamicModelRouter
except ImportError:
    from rate_limiter import TokenBucketRateLimiter
    from router import DynamicModelRouter

app = FastAPI(
    title="Enterprise Multi-Tenant GenAI Gateway",
    description="System Design implementation: Token Bucket rate limiting, intelligent model routing, and tenant quotas.",
    version="1.0.0"
)

limiter = TokenBucketRateLimiter(rpm_limit=30, tpm_limit=10000)

class GatewayRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    tenant_id: Optional[str] = "default_tenant"

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 30: GenAI System Design"}

@app.post("/api/v1/gateway/dispatch")
def dispatch_request(req: GatewayRequest):
    tenant = req.tenant_id
    estimated_tokens = max(10, len(req.prompt) // 3)

    # 1. Enforce Multi-tenant Token Bucket Rate Limit
    allowed, reason = limiter.consume(tenant, estimated_tokens)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={"error": "Rate Limit Exceeded", "reason": reason}
        )

    # 2. Dynamic Model Routing
    routing_decision = DynamicModelRouter.route_request(req.prompt)

    # 3. Simulated Model Completion
    completion = f"[{routing_decision['selected_model']}] Successfully served query for tenant '{tenant}'."

    return {
        "status": "success",
        "tenant_id": tenant,
        "tokens_allocated": estimated_tokens,
        "routing": routing_decision,
        "output": completion
    }
