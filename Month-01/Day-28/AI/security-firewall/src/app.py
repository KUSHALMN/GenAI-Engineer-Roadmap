from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

try:
    from .firewall import SecurityFirewall
except ImportError:
    from firewall import SecurityFirewall

app = FastAPI(
    title="GenAI Security Firewall & Injection Proxy",
    description="OWASP LLM Top 10 mitigation: injection scanner, canary tokens, and leak detection.",
    version="1.0.0"
)

firewall = SecurityFirewall()

class InspectRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

class InspectResponse(BaseModel):
    is_safe: bool
    threat_type: str = None
    details: str

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 28: GenAI Security"}

@app.post("/api/v1/security/inspect", response_model=InspectResponse)
def inspect_request(req: InspectRequest):
    result = firewall.inspect_prompt(req.prompt)
    if not result["is_safe"]:
        raise HTTPException(
            status_code=403,
            detail={"error": "Security Firewall Blocked Request", "threat": result}
        )
    return result

@app.post("/api/v1/security/verify_output")
def verify_output(payload: Dict[str, str]):
    completion = payload.get("completion", "")
    has_leak = firewall.inspect_completion_for_leak(completion)
    if has_leak:
        raise HTTPException(
            status_code=500,
            detail={"error": "Canary Token Exfiltration Detected! Output Quarantined."}
        )
    return {"status": "clean", "message": "No canary tokens detected"}
