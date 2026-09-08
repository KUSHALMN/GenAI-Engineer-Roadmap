from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

try:
    from .rate_limiter import TokenBucketRateLimiter
    from .router import DynamicModelRouter
except ImportError:
    from rate_limiter import TokenBucketRateLimiter
    from router import DynamicModelRouter

app = FastAPI(title="GenAI System Design Gateway - Day 30")
limiter = TokenBucketRateLimiter(rpm_limit=30, tpm_limit=10000)

class GatewayRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    tenant_id: Optional[str] = "default_tenant"

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 30: GenAI System Design"}

@app.post("/api/v1/gateway/dispatch")
def dispatch_request(req: GatewayRequest):
    allowed, reason = limiter.consume(req.tenant_id, max(10, len(req.prompt) // 3))
    if not allowed:
        raise HTTPException(status_code=429, detail={"error": reason})
    routing = DynamicModelRouter.route_request(req.prompt)
    return {
        "status": "success",
        "tenant_id": req.tenant_id,
        "routing": routing,
        "output": f"Served by {routing['selected_model']}"
    }
